import datetime


class DataProcessingError(Exception):
    pass


class DataProcessor:
    API_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def parse_cities(cls, data):
        cities = []
        for station in data:
            try:
                city = station["city"]
                if city:
                    cities.append((int(city["id"]),
                                   str(city["name"]).title(),
                                   str(city["commune"]["communeName"]).title(),
                                   str(city["commune"]["districtName"]).title(),
                                   str(city["commune"]["provinceName"]).title()))
            except (KeyError, ValueError) as e:
                raise DataProcessingError(f"Could't parse city data for {station}") from e

        return cities

    @classmethod
    def parse_stations(cls, data):
        stations = []
        for station in data:
            try:
                city_id = None if station["city"] is None else int(station["city"]["id"])
                stations.append((int(station["id"]),
                                 str(station["stationName"]),
                                 str(station["gegrLat"]),
                                 str(station["gegrLon"]),
                                 city_id,
                                 str(station["addressStreet"])))
            except (KeyError, ValueError) as e:
                raise DataProcessingError(f"Could't parse station data for {station}") from e
        return stations

    @classmethod
    def fill_params(cls, data):
        params = []
        for sensor in data:
            try:
                param = sensor["param"]
                params.append((int(param["idParam"]),
                               str(param["paramName"]),
                               str(param["paramFormula"]),
                               str(param["paramCode"])))
            except (KeyError, ValueError) as e:
                raise DataProcessingError(f"Could't parse station data for {sensor}") from e

    @classmethod
    def fill_sensors(cls, data):
        sensors = []
        for sensor in data:
            sensors.append((int(sensor["id"]),
                            int(sensor["stationId"]),
                            int(sensor["param"]["idParam"])))

    @classmethod
    def fill_data(cls, data, sensor_id):
        try:
            param_code = data["key"]
            insert_data = []
            for value in data["values"]:
                insert_data.append((sensor_id,
                                    param_code,
                                    int(datetime.datetime.strptime(value["date"], cls.API_DATE_FORMAT).timestamp()),
                                    str(value["value"])
                                    ))
        except (ValueError, KeyError) as e:
            raise DataProcessingError(f"Could't process data for {sensor_id}.") from e
        return insert_data


if __name__ == "__main__":
    pass
