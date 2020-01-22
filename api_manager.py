import requests
import logging_setup
import datetime
from db_manager import DbManager
from db_manager import DbManagerError

logger = logging_setup.get_logger("api_flow")

MAX_INTERVAL = 10 * 60

class ApiError(Exception):
    pass


class ApiManager:
    URL_BASE = "http://api.gios.gov.pl/pjp-api/rest"
    URL_STATIONS = "/station/findAll"
    URL_SENSORS = "/station/sensors"
    URL_DATA = "/data/getData"
    URL_AIR_QUALITY_INDEX = "/aqindex/getIndex"

    @classmethod
    def __call_api(cls, url):
        """
        Gets all information from specified url. Returns dict from json from response.

        :rtype: dict
        """
        try:
            response = requests.get(cls.URL_BASE + url)
            response.raise_for_status()
            DbManager.get_instance().insert_request_into_history(url)
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            raise ApiError("Could not get data from API.") from e
        return response.json()

    @classmethod
    def get_from_url(cls, url, parameter=None):
        """
        Calls endpoint with specified parameter.
        Returns json parsed to dictionary or None if request was made too early.

        :type url: str
        :type parameter: int
        :rtype: Union[dict, None]
        """
        # check if url belongs to ApiManager class (also deals with empty url)
        if url not in ApiManager.__dict__.values():
            raise ApiError("Provide correct url!")

        if type(parameter) is not int and url is not cls.URL_STATIONS:
            raise ApiError("Parameter has to be an integer and cannot be None!")

        parameter = "" if parameter is None else parameter
        target_url = f"{url}/{parameter}"

        try:
            request_valid = cls.validate_request(target_url)
        except DbManagerError as e:
            logger.exception(e)
            raise ApiError("Could't validate request") from e

        if request_valid:
            return cls.__call_api(target_url)
        else:
            return None

    @classmethod
    def validate_request(cls, url):
        request_timestamp = DbManager.get_instance().get_last_request(url)
        valid = datetime.datetime.now().timestamp() - request_timestamp >= 600
        logger.info(f"Request made for url: {url} is {'valid' if valid else 'invalid'}")
        return valid
