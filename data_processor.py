import datetime
from api_manager import ApiManager, ApiException


class DataManager:
    API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def fill_cities(cls, data):
        cities = []
        for station in data:
            city = station["city"]
            if city:
                cities.append((int(city["id"]),
                               city["name"],
                               city["commune"]["communeName"],
                               city["commune"]["districtName"],
                               city["commune"]["provinceName"]))
        return cities

    @classmethod
    def fill_stations(cls, data):
        stations = []
        for station in data:
            city_id = None if station["city"] is None else int(station["city"]["id"])
            stations.append((int(station["id"]),
                             station["stationName"],
                             station["gegrLat"],
                             station["gegrLon"],
                             city_id,
                             station["addressStreet"]))
        return stations

    @classmethod
    def fill_params(cls, data):
        params = []
        for sensor in data:
            param = sensor["param"]
            params.append((int(param["idParam"]),
                           param["paramName"],
                           param["paramFormula"],
                           param["paramCode"]))

    @classmethod
    def fill_sensors(cls, data):
        sensors = []
        for sensor in data:
            sensors.append((int(sensor["id"]),
                            int(sensor["stationId"]),
                            int(sensor["param"]["idParam"])))

    @classmethod
    def fill_data(cls, data, sensor_id):
        param_code = data["key"]
        insert_data = []
        for value in data["values"]:
            insert_data.append((sensor_id,
                                param_code,
                                int(datetime.datetime.strptime(value["date"], cls.API_DATE_FORMAT).timestamp()),
                                value["value"]
                                ))
        return insert_data

    @classmethod
    def insert_stations(cls):
        data = ApiManager.get_from_url(ApiManager.URL_DATA, 92)
        # print(cls.fill_cities(data))
        # print(cls.fill_stations(data))
        print(cls.fill_data(data, 92))


if __name__ == "__main__":
    DataManager.insert_stations()
