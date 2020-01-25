from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates


class GraphDrawer:
    """
    Responsible for drawing certain graphs. Uses matplotlib.
    """
    DISPLAY_DATE_FORMAT = "%d-%m, %H:%M"
    HOUR_INTERVAL = 6

    FORMAT = {
        "C6H6": ["#ff0000", r"C$_{6}$H$_{6}$"],
        "CO": ["#0e0e42", "CO"],
        "NO2": ["#2e8a03", r"NO$_{2}$"],
        "PM10": ["#828282", "PM10"],
        "PM2.5": ["#66573d", "PM2.5"],
        "O3": ["#27c6d1", r"O$_{3}$"],
        "SO2": ["#ffa70f", r"SO$_{2}$"]
    }

    DISTINCT_COLORS = [
        '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
    ]

    @classmethod
    def __draw_graph(cls, x_label="Czas", y_label="Wartość"):
        """
        Draws graph for data_plot with given labels.

        :param x_label: str
        :param y_label: str
        """
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter(cls.DISPLAY_DATE_FORMAT)
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.gca().xaxis.set_major_locator(mpl_dates.HourLocator(interval=cls.HOUR_INTERVAL))
        plt.tight_layout()
        plt.legend()
        plt.show()

    @classmethod
    def draw_station_graph(cls, station_name, sensors_data):
        """
        Draws graph for station with station name and given data for station's sensors.
        :param station_name: str
        :param sensors_data: dict
        """
        plt.title(f"Dane dla stacji pomiarowej: {station_name}")
        for series_name, data in sensors_data.items():
            color, lbl = cls.FORMAT[series_name]
            plt.plot_date(data[0], data[1], color=color,
                          label=lbl, linestyle="solid", marker=",")
        cls.__draw_graph()

    @classmethod
    def draw_sensor_graph(cls, sensor_code, stations_data):
        """
        Draws graph for sensor with sensor code and given data for sensor's station data.

        :param sensor_code: str
        :param stations_data: dict
        """
        plt.title(f"Dane dla stanowiska pomiarowego {cls.FORMAT[sensor_code][1]}")
        for color, (stat_name, (time_data, sensor_data)) in zip(cls.DISTINCT_COLORS, stations_data.items()):
            plt.plot_date(time_data, sensor_data, color=color,
                          label=stat_name, linestyle="solid", marker=",")
        cls.__draw_graph()