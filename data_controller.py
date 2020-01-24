from data_manager import DataManager
from data_manager import DataManagerError
from data_processor import DataProcessingError
from data_processor import DataProcessor
from db_manager import DbManagerError
from db_manager import DbManager
from graph_drawer import GraphDrawer
import datetime
import logging_setup

logger = logging_setup.get_logger("data_flow")


class DataController:
    """
    This class is a controller for all classes responsible for processing data. It controls data flow.
    """

    @classmethod
    def get_essential_data(cls):
        """
        Get data for cities, stations and sensors from API and inserts it to Database. Logs all errors.
        """
        try:
            raw_data = DataManager.get_from_url(DataManager.URL_STATIONS)
            if raw_data:
                cities = DataProcessor.parse_cities(raw_data)
                stations = DataProcessor.parse_stations(raw_data)

                sensors = []
                for station in stations:
                    id_station = station[0]
                    raw_sensors = DataManager.get_from_url(DataManager.URL_SENSORS, id_station)
                    if raw_sensors:
                        new_sensors = DataProcessor.parse_sensors(raw_sensors)
                        sensors.extend(new_sensors)


                db.insert_from_list("cities", cities, replace=True)
                db.insert_from_list("stations", stations, replace=True)
                db.insert_from_list("sensors", sensors, replace=True)
                return True
            return False

        except (DataManagerError, DataProcessingError, DbManagerError) as e:
            logger.exception(e)

    @classmethod
    def get_all_data_for_station(cls, station_id):
        sensors = DbManager.get_instance().get_all_sensors(station_id)
        for sensor in sensors:
            sensor_id = sensor[0]
            sensor_key = sensor[1]
            raw_sensor_data = DataManager.get_from_url(DataManager.URL_DATA, sensor_id)
            if raw_sensor_data:
                if sensor_key != raw_sensor_data["key"]:
                    logger.error(
                        f"Data for {sensor} is invali. Sensor key: {sensor_key} vs APi key {raw_sensor_data['key']}")
                else:
                    parsed_data = DataProcessor.parse_sensor_data(raw_sensor_data, sensor_id)
                    DbManager.get_instance().insert_api_data(parsed_data)

    @classmethod
    def single_station_for_graph(cls, station_id, excluded_sensors=None):
        db = DbManager()
        data = db.get_all_data_for_station(station_id)
        grouped_data = {k[0]: [[], []] for k in data}
        for row in data:
            grouped_data[row[0]][0].append(datetime.datetime.fromtimestamp(row[1]))
            grouped_data[row[0]][1].append(float(row[2]))

        # del grouped_data["CO"]
        # del grouped_data["NO2"]
        del grouped_data["PM10"]

        GraphDrawer.draw_station_graph(db.station_name_by_id(station_id)[0][0], grouped_data)




