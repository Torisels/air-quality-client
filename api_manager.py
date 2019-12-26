import requests


class ApiException(Exception):
    pass


class ApiManager:
    URL_BASE = "http://api.gios.gov.pl/pjp-api/rest"
    URL_STATIONS = "/station/findAll"
    URL_SENSORS = "/station/sensors"
    URL_DATA = "/data/getData"
    URL_AIR_QUALITY_INDEX = "/aqindex/getIndex"

    @classmethod
    def call_api(cls, url):
        """
        Gets all stations from /station/findALl endpoint of GIOŚ API. Returns json parsed to dictionary

        :rtype: dict
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Could not get data from GIOŚ API.") from e
        return response.json()

    @classmethod
    def get_from_url(cls, url, parameter=None):
        """
        Calls endpoint with specified parameter.
        Returns json parsed to dictionary.

        :type url: str
        :type parameter: int
        :rtype: dict
        """
        # check if url belongs to ApiManager class (also deals with empty url)
        if url not in ApiManager.__dict__.values():
            raise ValueError("Provide correct url!")

        if type(parameter) is not int and url != cls.URL_STATIONS:
            raise ValueError("Parameter has to be an integer and cannot be None!")

        parameter = "" if parameter is None else parameter
        target_url = f"{cls.URL_BASE}{url}/{parameter}"
        return cls.call_api(target_url)
