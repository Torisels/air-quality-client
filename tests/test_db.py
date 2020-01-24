import pytest
from db_manager import DbManager
from db_manager import DbManagerError


def test_run_sql():
    db = DbManager()
    with pytest.raises(DbManagerError) as error_info:
        db.run_sql("blablala1")
        db.run_sql("INSERT INTO data VALUES (?,?,?,?)", [(1, 2, 3, 4)])
        db.run_sql("INSERT INTO cities VALUES (?,?,?,?,?)", [(3, "4", "5", "6", "&")])


test_data = [(99999, 0), ("abc", 0)]


@pytest.mark.parametrize("stat_id, expected", test_data)
def test_get_sensors_by_station_id(stat_id, expected):
    db = DbManager()

    result = db.get_sensor_by_station_id(stat_id)
    assert type(result) == list
    assert len(result) == expected

    with pytest.raises(DbManagerError):
        db.get_sensor_by_station_id("")
        db.get_sensor_by_station_id(None)

def test_get_all_stations_by_param():
    db = DbManager()
    result = db.get_all_stations_by_param("CO")
    assert len(result) > 1
    assert type(result) == list


def test_get_data_by_sensors_ids():
    db = DbManager()
    result = db.get_data_by_sensors_ids([3575, 3576])
    assert len(result) == 120
    assert type(result) == list