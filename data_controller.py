from api_manager import ApiManager
from api_manager import ApiError
from data_processor import DataProcessingError
from data_processor import DataProcessor
from db_manager import DbManagerError
from db_manager import DbManager
import logging.config
import yaml

# logging setup
with open('logging.yaml', 'r') as f:
    log_cfg = yaml.safe_load(f.read())

logging.config.dictConfig(log_cfg)
logger = logging.getLogger('data_flow')


class DataController:
    """
    This class is a controller for all classes responsible for processing data.
    """

    @classmethod
    def insert_cities_stations(cls):
        """
        Get data for cities and stations from API and inserts it to Database. Logs all errors.
        """
        try:
            raw_data = ApiManager.get_from_url(ApiManager.URL_STATIONS)
            cities = DataProcessor.parse_cities(raw_data)
            stations = DataProcessor.parse_stations(raw_data)
            db = DbManager.get_instance()
            db.insert_from_list("cities", cities, replace=True)
            db.insert_from_list("stations", stations, replace=True)

        except (ApiError, DataProcessingError, DbManagerError) as e:
            logger.exception(e)


if __name__ == "__main__":
    DataController.insert_cities_stations()
