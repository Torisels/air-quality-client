import pytest
import json
from data_processor import DataProcessor
from data_processor import DataProcessingError


def test_parse_data():
    with open("test_data_data.json") as f:
        data = json.load(f)

    result = DataProcessor.parse_sensor_data(data, 92)
    assert type(result) == list
    assert len(result) > 1
