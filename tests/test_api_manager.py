from api_manager import ApiManager
from api_manager import ApiError
import pytest


def test_get_from_url():

    with pytest.raises(ApiError) as e_info:
        ApiManager.get_from_url("")
        ApiManager.get_from_url("asdef")
        ApiManager.get_from_url("http://google.com")

    with pytest.raises(ApiError, match="Provide correct url!") as e_info:
        ApiManager.get_from_url("")
        ApiManager.get_from_url("ads")

    with pytest.raises(ApiError, match="Parameter has to be an integer and cannot be None!") as e_info:
        ApiManager.get_from_url(ApiManager.URL_DATA)
        ApiManager.get_from_url(ApiManager.URL_DATA, "2")

    result = ApiManager.get_from_url(ApiManager.URL_STATIONS)
    assert type(result) == list
    assert len(result) > 0

    result = ApiManager.get_from_url(ApiManager.URL_SENSORS, 14)
    assert type(result) == list
    assert result[0]["id"] == 92
    assert result[0]["stationId"] == 14

    result = ApiManager.get_from_url(ApiManager.URL_DATA, 92)
    assert type(result) == dict
    assert result["key"] == "PM10"
    assert type(result["values"]) == list
    assert len(result["values"]) > 0
    assert "date" in result["values"][0]

