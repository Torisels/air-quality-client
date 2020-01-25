from data_manager import DataManager, DataManagerError, ApiError
from db_manager import DbManager, DbManagerError
from graph_drawer import GraphDrawer
import pytest


def test_get_from_api():
    data_manager = DataManager(DbManager())

    with pytest.raises(ApiError) as e_info:
        data_manager.call_api("")
        data_manager.call_api("asdef")
        data_manager.call_api("http://google.com")

    with pytest.raises(ApiError) as e_info:
        data_manager.call_api(DataManager.URL_DATA)

    result = data_manager.call_api(data_manager.URL_STATIONS)
    assert type(result) == list
    assert len(result) > 0

    result = data_manager.call_api(f"{DataManager.URL_DATA}/92")
    assert type(result) == dict
    assert result["key"] == "PM10"
    assert type(result["values"]) == list
    assert len(result["values"]) > 0
    assert "date" in result["values"][0]


def test_get_stations():
    data_manager = DataManager(DbManager())
    result = data_manager.get_stations()
    assert type(result) == list
    assert len(result) > 0

    result = data_manager.get_stations(531)
    assert type(result) == tuple
    assert len(result) == 7


def test_prepare_necessary_data():
    data_manager = DataManager(DbManager())
    result = data_manager.prepare_necessary_data()
    assert len(result) > 0
    assert type(result) == list


def test_get_data_by_station_ids_for_graphing():
    data_manager = DataManager(DbManager())
    result = data_manager.get_data_by_station_ids_for_graphing([530, 538, 550], "PM10")
    assert len(result) == 3
