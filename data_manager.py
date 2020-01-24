import requests
import logging_setup
import datetime
from db_manager import DbManager, DbManagerError
from data_processor import DataProcessor, DataProcessingError

logger = logging_setup.get_logger("api_flow")


class DataManagerError(Exception):
    pass


class ApiError(Exception):
    pass


class DataManager:
    MAX_CACHE_INTERVAL = 600
    URL_BASE = "http://api.gios.gov.pl/pjp-api/rest"
    URL_STATIONS = '/station/findAll'
    URL_SENSORS = "/station/sensors"
    URL_DATA = "/data/getData"

    def __init__(self, db_obj):
        """
        :type db_obj: DbManager
        """
        self.db = db_obj

    def request_is_valid(self, url):
        """
        Validates request for cache control.
        Returns false if request was made less than 10 minutes ago or True if opposite.

        :param url: str
        :return: bool
        """
        try:
            request_timestamp = self.db.get_last_request(url)
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error performing cache query") from e
        if request_timestamp:
            valid = datetime.datetime.now().timestamp() - request_timestamp >= self.MAX_CACHE_INTERVAL
        else:
            valid = True
        logger.info(f"Request made for url: {url} is {'valid' if valid else 'invalid'}")
        return valid

    def prepare_url(self, url, parameter=None):
        """
        Prepares url for API call.

        :type url: str
        :type parameter: int
        :rtype: str
        """
        # check if url belongs to ApiManager class (also deals with empty url)
        if url not in DataManager.__dict__.values():
            raise DataManagerError("Provide correct url!")

        if type(parameter) is not int and url is not self.URL_STATIONS:
            raise DataManagerError("Parameter has to be an integer and cannot be None!")

        parameter = "" if parameter is None else f"/{parameter}"
        target_url = f"{url}{parameter}"

        return target_url

    def call_api(self, url):
        """
        Gets all information from specified url. Returns dict from json response.
        Inserts endpoint to cache history in database.
        :rtype: list
        """
        try:
            response = requests.get(self.URL_BASE + url)
            response.raise_for_status()
            self.db.insert_request_into_history(url)
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            raise ApiError("Could not get data from API.") from e
        return response.json()

    def get_stations(self, station_id=None):
        url = self.prepare_url(self.URL_STATIONS)

        if self.request_is_valid(url):
            try:
                raw_data = self.call_api(url)
                cities = DataProcessor.parse_cities(raw_data)
                stations = DataProcessor.parse_stations(raw_data)
                self.db.insert_from_list("cities", cities, True)
                self.db.insert_from_list("stations", stations, True)
            except (ApiError, DataProcessingError, DbManagerError) as e:
                raise DataManagerError("Could not handle data properly") from e
        try:
            stations = self.db.get_all_station_data(station_id)
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error when obtaining data from db") from e

        if station_id:
            return stations[0]

        return stations

    def get_sensors(self, station_id, get_results=True):
        url = self.prepare_url(self.URL_SENSORS, station_id)
        if self.request_is_valid(url):
            try:
                raw_sensor_data = self.call_api(url)
                if len(raw_sensor_data) > 0:
                    sensor_data = DataProcessor.parse_sensors(raw_sensor_data)
                    self.db.insert_from_list("sensors", sensor_data, replace=True)
            except (ApiError, DataProcessingError, DbManagerError) as e:
                raise DataManagerError("Could not handle data properly") from e

        if get_results:
            try:
                sensors = self.db.get_sensor_by_station_id(station_id)
            except DbManagerError as e:
                logger.exception(e)
                raise DataManagerError("Error when obtaining data from db") from e

            return sensors

    def prepare_necessary_data(self):
        stations = self.get_stations()
        for station in stations:
            stat_id = station[6]
            self.get_sensors(stat_id, False)
        return stations

    def get_all_sensors_for_view(self):
        return self.db.get_all_params()

    def get_all_stations_by_param(self, param):
        try:
            data = self.db.get_all_stations_by_param(param)
            return data
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error getting data") from e
