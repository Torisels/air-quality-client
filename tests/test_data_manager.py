from data_manager import DataManager, DataManagerError
from db_manager import DbManager, DbManagerError
import pytest


def test_get_from_api():
    data_manager = DataManager(DbManager())

    with pytest.raises(DataManagerError) as e_info:
        data_manager.get_from_api("")
        data_manager.get_from_api("asdef")
        data_manager.get_from_api("http://google.com")

    with pytest.raises(DataManagerError) as e_info:
        data_manager.get_from_api("")
        data_manager.get_from_api("ads")

    with pytest.raises(DataManagerError) as e_info:
        data_manager.get_from_api(DataManager.URL_DATA)
        data_manager.get_from_api(DataManager.URL_DATA, "2")

    result = data_manager.get_from_api(data_manager.URL_STATIONS)
    assert type(result) == list
    assert len(result) > 0

    result = data_manager.get_from_api(DataManager.URL_SENSORS, 14)
    assert type(result) == list
    assert result[0]["id"] == 92
    assert result[0]["stationId"] == 14

    result = data_manager.get_from_api(DataManager.URL_DATA, 92)
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
    assert len(result) == 9


def test_prepare_necessary_data():
    data_manager = DataManager(DbManager())
    result = data_manager.prepare_necessary_data()
    assert len(result) > 0
    assert type(result) == list

