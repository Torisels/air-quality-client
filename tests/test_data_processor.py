import pytest
import json
from data_processor import DataProcessor
from data_processor import DataProcessingError


def test_parse_data():
    with open("test_data_data.json") as f:
        data = json.load(f)

    data = data[test_parse_data.__name__]
    result = DataProcessor.parse_sensor_data(data[0], 92)
    assert type(result) == list
    assert len(result) == 2

    result = DataProcessor.parse_sensor_data(data[1], 92)
    assert type(result) == list
    assert len(result) == 1

    result = DataProcessor.parse_sensor_data(data[2], 92)
    assert type(result) == list
    assert len(result) == 1

    with pytest.raises(DataProcessingError):
        DataProcessor.parse_sensor_data(data[3], 92)


def test_parse_stations():
    with open("test_data_data.json") as f:
        data = json.load(f)
    data = data[test_parse_stations.__name__]
    result = DataProcessor.parse_stations(data)
    assert type(result) == list
    assert len(result) == 1