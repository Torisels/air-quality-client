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
        "03": ["#27c6d1", r"O$_{3}$"],
        "SO2": ["#ffa70f", r"SO$_{2}$"]
    }

    @classmethod
    def draw_graph(cls, title_g, dates, y_series):
        date_times = [datetime.datetime.fromtimestamp(t) for t in dates]
        plt.title(r'This is an expression C$_{6}$H$_{6}$')
        plt.plot_date(date_times, y_series, linestyle="solid")
        plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter("%d-%m, %H:%M")
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.tight_layout()
        plt.show()

    @classmethod
    def draw_station_graph(cls, station_name, sensors_data):
        plt.title(f"Dane dla stacji pomiarowej: {station_name}")
        for series_name, data in sensors_data.items():
            color, lbl = cls.FORMAT[series_name]
            plt.plot_date(data[0], data[1], color=color,
                          label=lbl, linestyle="solid", marker=",")

        plt.xlabel("Czas")
        plt.ylabel("Wartość")
        plt.gcf().autofmt_xdate()
        date_format = mpl_dates.DateFormatter(cls.DISPLAY_DATE_FORMAT)
        plt.gca().xaxis.set_major_formatter(date_format)
        plt.tight_layout()
        plt.legend()
        plt.show()


if __name__ == "__main__":
    data = DbManager.get_instance().get_data(3575)
    b = list(zip(*data[:10]))
    GraphDrawer.draw_graph("abc", b[0], [float(val) for val in b[1]])
