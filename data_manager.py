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
    """Responsible for all data flow in application."""
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
        :rtype: Union[list, dict]
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
        """
        Gets all station data from API and inserts it into database.

        :param station_id: int
        :return: Union[list, tuple]
        """
        url = self.prepare_url(self.URL_STATIONS)

        if self.request_is_valid(url):
            try:
                raw_data = self.call_api(url)
                cities = DataProcessor.parse_cities(raw_data)
                stations = DataProcessor.parse_stations(raw_data)
                self.db.insert_from_list("cities", cities, True)
                self.db.insert_from_list("stations", stations, True)
            except (ApiError, DataProcessingError, DbManagerError) as e:
                raise DataManagerError("Could not handle API data properly") from e
        try:
            stations = self.db.get_all_station_data(station_id)
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error when obtaining data from database!") from e

        if station_id:
            return stations[0]

        return stations

    def get_sensors(self, station_id, get_results=True):
        """
        Gets all sensors for given station id from API and inserts it into database.

        :param station_id: int
        :param get_results: bool
        :return: list
        """
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
                sensors = self.db.get_sensors_by_station_id(station_id)
            except DbManagerError as e:
                logger.exception(e)
                raise DataManagerError("Error when obtaining data from db") from e

            return sensors

    def prepare_necessary_data(self):
        """
        Prepares all necessary data for running an application. Gets all stations and sensors.

        :return: list
        """
        stations = self.get_stations()
        for station in stations:
            stat_id = station[6]
            self.get_sensors(stat_id, False)
        return stations

    def get_all_sensors_for_view(self):
        """
        Gets all types of sensors from db and returns it in UI suitable format.
        :return: list
        """
        return self.db.get_all_params()

    def get_all_stations_by_param(self, param):
        """
        Gets all stations from database by given param(ex. CO, NO2)

        :param param: str
        :return: list
        """
        try:
            data = self.db.get_all_stations_by_param(param)
            return data
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error getting data") from e

    def __insert_sensors_data_to_db(self, sensors):
        """
        Gets data by sensor id from API and inserts it into db.
        :param sensors: list
        """
        for s_id in sensors:
            url = self.prepare_url(self.URL_DATA, s_id)
            if self.request_is_valid(url):
                try:
                    raw_data = self.call_api(url)
                    parsed_data = DataProcessor.parse_sensor_data(raw_data, s_id)
                    if len(parsed_data) != 0:
                        self.db.insert_api_data(parsed_data)
                except (ApiError, DbManagerError, DataProcessingError) as e:
                    logger.exception(e)
                    raise DataManagerError("Error occurred when processing API data") from e

    def get_data_by_sensor_ids_for_graphing(self, sensors):
        """
        :type sensors: set
        :rtype: list[int]
        """
        self.__insert_sensors_data_to_db(sensors)
        try:
            sensor_data = self.db.get_data_by_sensors_ids(sensors)
            if len(sensor_data) == 0:
                raise DataManagerError("Db returned empty list")

            return self.group_data(sensor_data)
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Error obtaining data from Database") from e

    @staticmethod
    def group_data(sensor_data):
        """
        Groups data by it's main key that it can suit into GraphDrawer.

        :param sensor_data: list(tuple)
        :return: dict
        """
        grouped_data = {k[0]: [[], []] for k in sensor_data}
        for row in sensor_data:
            grouped_data[row[0]][0].append(datetime.datetime.fromtimestamp(row[1]))
            grouped_data[row[0]][1].append(float(row[2]))
        return grouped_data

    def get_data_by_station_ids_for_graphing(self, stations, param_code):
        """
        Gets data for graph for specified stations and one sensor type.

        :param stations: set
        :param param_code: str
        :return: dict
        """
        try:
            sensors = self.db.get_sensors_by_stations_ids_sensor_code(stations, param_code)
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError("Could not obtain sensor list for selected stations") from e
        if len(sensors) == 0:
            raise DataManagerError("Sensors for station can't be empty")
        sensors = list(zip(*sensors))[0]
        self.__insert_sensors_data_to_db(sensors)
        data = self.db.get_data_by_stations_ids(stations, param_code)
        return self.group_data(data)

    def get_station_name_by_id(self, station_id):
        """
        Gets station name from database by it's id.
        :param station_id: str
        :return: str
        """
        try:
            return self.db.station_name_by_id(station_id)[0][0]
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError from e

    def delete_cache(self):
        """
        Deletes all cache from database.
        """
        try:
            self.db.delete_cache()
        except DbManagerError as e:
            logger.exception(e)
            raise DataManagerError from e