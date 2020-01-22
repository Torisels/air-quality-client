from api_manager import ApiManager
from api_manager import ApiError
from data_processor import DataProcessingError
from data_processor import DataProcessor
from db_manager import DbManagerError
from db_manager import DbManager
import logging_setup

logger = logging_setup.get_logger("data_flow")


class DataController:
    """
    This class is a controller for all classes responsible for processing data. It controls data flow.
    """

    @classmethod
    def insert_obligatory_data(cls):
        """
        Get data for cities, stations and sensors from API and inserts it to Database. Logs all errors.
        """
        try:
            raw_data = ApiManager.get_from_url(ApiManager.URL_STATIONS)
            if raw_data:
                cities = DataProcessor.parse_cities(raw_data)
                stations = DataProcessor.parse_stations(raw_data)

                sensors = []
                for station in stations:
                    id_station = station[0]
                    raw_sensors = ApiManager.get_from_url(ApiManager.URL_SENSORS, id_station)
                    if raw_sensors:
                        new_sensors = DataProcessor.parse_sensors(raw_sensors)
                        sensors.extend(new_sensors)

                db = DbManager.get_instance()
                db.insert_from_list("cities", cities, replace=True)
                db.insert_from_list("stations", stations, replace=True)
                db.insert_from_list("sensors", sensors, replace=True)
                return True
            return False

        except (ApiError, DataProcessingError, DbManagerError) as e:
            logger.exception(e)


if __name__ == "__main__":
    DataController.insert_obligatory_data()
