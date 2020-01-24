import datetime
import logging_setup

logger = logging_setup.get_logger("data_parsing")


class DataProcessingError(Exception):
    pass


class DataProcessor:
    """It is responsible for processing data from the API to suitable format for database.
    If error is occurred during parsing data it is being ignored and then logged into data_parsing.log
    """
    API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def parse_cities(cls, data):
        """
        Parses data from API/stations for cities.

        :type data: list
        :rtype: list
        """
        cities = []
        for station in data:
            try:
                city = station["city"]
                if city:
                    cities.append((int(city["id"]),
                                   str(city["name"]).title(),
                                   str(city["commune"]["communeName"]).title(),
                                   str(city["commune"]["districtName"]).title(),
                                   str(city["commune"]["provinceName"]).title()))
            except (KeyError, ValueError) as e:
                logger.exception(e)

        return cities

    @classmethod
    def parse_stations(cls, data):
        """
        Parses data from API/stations for stations.

        :type data: list
        :rtype: list
        """
        stations = []
        for station in data:
            try:
                city_id = None if station["city"] is None else int(station["city"]["id"])
                stations.append((int(station["id"]),
                                 str(station["stationName"]),
                                 str(station["gegrLat"]),
                                 str(station["gegrLon"]),
                                 city_id,
                                 str(station["addressStreet"])))
            except (KeyError, ValueError) as e:
                logger.exception(e)
        return stations

    @classmethod
    def parse_sensors(cls, data):
        """
        Parses data from API/sensors for sensor.

        :type data: list
        :rtype: list
        """
        sensors = []
        for sensor in data:
            try:
                sensors.append((int(sensor["id"]),
                                int(sensor["stationId"]),
                                str(sensor["param"]["paramCode"])))
            except (KeyError, ValueError) as e:
                logger.exception(e)
        return sensors

    @classmethod
    def parse_sensor_data(cls, data, sensor_id):
        """
        Parses data from API/data for sensor's data.

        :type data: dict
        :type sensor_id: int
        :rtype: list
        """
        insert_data = []
        try:
            param_code = str(data["key"])
        except KeyError as e:
            logger.exception(e)
            raise DataProcessingError("No key provided in data") from e
        for value in data["values"]:
            try:
                timestamp = datetime.datetime.strptime(value["date"], cls.API_DATE_FORMAT).timestamp()
                insert_data.append((hash((sensor_id, timestamp)),
                                    sensor_id,
                                    param_code,
                                    timestamp,
                                    str(float(value["value"]))
                                    ))
            except (ValueError, KeyError, TypeError) as e:
                logger.exception(e)
        return insert_data

