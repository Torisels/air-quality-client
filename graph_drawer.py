from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from db_manager import DbManager
import datetime


class GraphDrawer:
    DISPLAY_DATE_FORMAT = "%d-%m, %H:%M"

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
        '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
        '#ffffff', '#000000'
    ]

    @classmethod
    def __draw_graph(cls, x_label, y_label):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter(cls.DISPLAY_DATE_FORMAT)
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.tight_layout()
        plt.legend()
        plt.show()

    @classmethod
    def draw_station_graph(cls, station_name, sensors_data):
        plt.title(f"Dane dla stacji pomiarowej: {station_name}")
        for series_name, data in sensors_data.items():
            color, lbl = cls.FORMAT[series_name]
            plt.plot_date(data[0], data[1], color=color,
                          label=lbl, linestyle="solid", marker=",")

        cls.__draw_graph("Czas", "Wartość")

    @classmethod
    def draw_sensor_graph(cls, sensor_code, stations_data):
        plt.title(f"Dane dla stanowiska pomiarowego {cls.FORMAT[sensor_code][1]}")
        for color, (stat_name, (time_data, sensor_data)) in zip(cls.DISTINCT_COLORS, stations_data.items()):
            print(stat_name)

    @classmethod
    def draw_simple_graph(cls):

        plt.title("graph1")
        plt.plot([1,2,3,4,5],[10,20,30,40,50])
        plt.show()

if __name__ == "__main__":
    data = DbManager.get_instance().get_data(3575)
    b = list(zip(*data[:10]))
    GraphDrawer.draw_graph("abc", b[0], [float(val) for val in b[1]])
