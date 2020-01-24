from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from data_manager import DataManager
from db_manager import DbManager
from graph_drawer import GraphDrawer
from collections import defaultdict
import sys


class UiMainWindow:
    MODE_STATION = 0
    MODE_SENSOR = 1

    def __init__(self, d_manager: DataManager):
        self.thread_pool = QThreadPool()
        self.data_manager = d_manager
        self.selected_sensors = defaultdict(set)
        self.selected_stations = defaultdict(set)
        self.mode = self.MODE_STATION
        self.station_data = None
        self.current_param = None
        self.current_station = None

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(832, 713)

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 800, 391))
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setColumnHidden(7, True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)

        self.params_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.params_widget.setGeometry(QtCore.QRect(10, 420, 318, 231))
        self.params_widget.setRowCount(0)
        self.params_widget.setObjectName("params_widget")
        self.params_widget.setColumnCount(4)
        self.params_widget.setColumnHidden(3, True)

        self.params_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.params_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        item = QtWidgets.QTableWidgetItem()
        self.params_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.params_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.params_widget.setHorizontalHeaderItem(2, item)

        self.main_label = QLabel(self.centralwidget)
        self.main_label.setGeometry(QtCore.QRect(10, 400, 500, 16))
        self.main_label.setObjectName("main_label")

        self.push_button_draw_graph = QPushButton(self.centralwidget)
        self.push_button_draw_graph.setGeometry(QtCore.QRect(30, 660, 171, 23))
        self.push_button_draw_graph.setObjectName("push_button_draw_graph")
        self.push_button_draw_graph.clicked.connect(self.draw_graph_button_clicked)
        self.push_button_draw_graph.setDisabled(True)

        self.push_button_download_data = QPushButton(self.centralwidget)
        self.push_button_download_data.setGeometry(QtCore.QRect(450, 450, 141, 61))
        self.push_button_download_data.setObjectName("push_button_download_data")
        self.push_button_download_data.clicked.connect(self.start_download_data)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(450, 520, 141, 61))
        self.pushButton_3.setObjectName("pushButton_3")

        self.layout_widget_radio_buttons = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_radio_buttons.setGeometry(QtCore.QRect(460, 590, 160, 61))
        self.layout_widget_radio_buttons.setObjectName("layout_widget_radio_buttons")

        self.layout_radio_buttons = QtWidgets.QVBoxLayout(self.layout_widget_radio_buttons)
        self.layout_radio_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout_radio_buttons.setObjectName("layout_radio_buttons")

        self.radioButton = QtWidgets.QRadioButton(self.layout_widget_radio_buttons)
        self.radioButton.setObjectName("radioButton")
        self.layout_radio_buttons.addWidget(self.radioButton)
        self.radioButton.setChecked(True)
        self.radioButton.toggled.connect(self.radio_button_on_click)

        self.radioButton_2 = QtWidgets.QRadioButton(self.layout_widget_radio_buttons)
        self.radioButton_2.setObjectName("radioButton_2")
        self.layout_radio_buttons.addWidget(self.radioButton_2)

        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        self.radioButton_2.setDisabled(True)

        self.radio_button_on_click()

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Klient jakości powietrza"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nazwa stacji"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Długość geo."))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Szerokość geo."))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Miasto"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Adres"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Województwo"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Użyj"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Id"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        item = self.params_widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Użyj"))
        item = self.params_widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nazwa"))
        item = self.params_widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Symbol"))
        self.main_label.setText(_translate("MainWindow", "Stanowiska pomiarowe dla wybranej stacji"))
        self.push_button_draw_graph.setText(_translate("MainWindow", "Rysuj wykres dla stacji"))
        self.push_button_download_data.setText(_translate("MainWindow", "Pobierz dane"))
        self.pushButton_3.setText(_translate("MainWindow", "Usuń historię zapytań"))
        self.radioButton.setText(_translate("MainWindow", "Tryb jednej stacji"))
        self.radioButton_2.setText(_translate("MainWindow", "Tryb jednego stanowiska"))

    @staticmethod
    def add_checkbox_to_table(table: QTableWidget, row, col, checked=False):
        check_box_item = QtWidgets.QTableWidgetItem()
        check_box_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if checked:
            check_box_item.setCheckState(QtCore.Qt.Checked)
        else:
            check_box_item.setCheckState(QtCore.Qt.Unchecked)
        table.setItem(row, col, check_box_item)

    def draw_graph_button_clicked(self):
        if self.mode == self.MODE_STATION:
            sensors = self.selected_sensors[self.current_station]
            data = self.data_manager.get_data_by_sensor_ids_for_graphing(sensors)
            station_name = self.data_manager.get_station_name_by_id(self.current_station)
            GraphDrawer.draw_station_graph(station_name, data)


    def generate_station_view(self, stations=None):
        self.station_data = stations
        self.tableWidget.setRowCount(len(stations))
        self.tableWidget.setColumnHidden(7, True)
        for row, station in enumerate(stations):
            if self.mode == self.MODE_SENSOR:
                checked = True if station[6] in self.selected_stations[self.current_param] else False
                self.add_checkbox_to_table(self.tableWidget, row, 6, checked)
            for col, parameter in enumerate(station):
                if col == 6:
                    col += 1
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setText(str(parameter))
                self.tableWidget.setItem(row, col, item)

        self.tableWidget.itemClicked.connect(self.handle_table_item_clicked)

    def handle_table_item_clicked(self, item):
        item_row = item.row()
        station_id = int(self.tableWidget.item(item_row, 7).text())
        if self.mode == self.MODE_STATION:
            data = self.data_manager.get_sensors(int(station_id))
            self.generate_sensor_table_view(data)
            self.current_station = station_id
        else:
            if item.checkState() == QtCore.Qt.Checked:
                self.selected_stations[self.current_param].add(station_id)
            elif item.checkState is not QtCore.Qt.Unchecked and item.column() == 6:
                self.selected_stations[self.current_param].discard(station_id)

    def generate_sensor_table_view(self, data):
        self.params_widget.setRowCount(len(data))
        for row, sensor in enumerate(data):
            if self.mode == self.MODE_STATION:
                checked = True if sensor[2] in self.selected_sensors else False
                self.add_checkbox_to_table(self.params_widget, row, 0, checked)
            for column, element in enumerate(sensor):
                column += 1
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setText(str(element))
                self.params_widget.setItem(row, column, item)
        self.params_widget.itemClicked.connect(self.handle_sensor_table_item_clicked)

    def handle_sensor_table_item_clicked(self, item: QCheckBox):
        if self.mode == self.MODE_STATION:
            sensor_id = int(self.params_widget.item(item.row(), 3).text())
            if item.checkState() == QtCore.Qt.Checked:
                self.selected_sensors[self.current_station].add(sensor_id)
            elif item.checkState is not QtCore.Qt.Unchecked and item.column() == 0:
                self.selected_sensors[self.current_station].discard(sensor_id)
            if len(self.selected_sensors[self.current_station]) >0:
                self.push_button_draw_graph.setDisabled(False)
            else:
                self.push_button_draw_graph.setDisabled(True)
        else:
            param_code = self.params_widget.item(item.row(), 2).text()
            self.current_param = param_code
            data = self.data_manager.get_all_stations_by_param(param_code)
            self.generate_station_view(data)

    def radio_button_on_click(self):
        if self.radioButton.isChecked():
            self.mode = self.MODE_STATION
            self.tableWidget.setColumnHidden(6, True)
            self.main_label.setText("Tryb jednej stacji. Poniżej znajduje się lista dostępnych stanowisk pomiarowych: ")
            self.push_button_draw_graph.setText("Rysuj wykres dla stacji")
            self.params_widget.setRowCount(0)
            if self.station_data:
                self.generate_station_view(self.station_data)
        else:
            if self.station_data is None:
                self.radioButton_2.toggle()
                self.radioButton.toggle()
            self.mode = self.MODE_SENSOR
            self.main_label.setText("Tryb jednego stanowiska pomiarowego. Proszę wybrać stacje pomiarowe (limit: 20)")
            self.push_button_draw_graph.setText("Rysuj wykres dla stanowiska")
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnHidden(6, False)
            self.params_widget.setColumnHidden(0, True)

            data = self.data_manager.get_all_sensors_for_view()
            self.generate_sensor_table_view(data)

    def update_ui_after_data_finished(self):
        self.push_button_download_data.setText("Pobierz dane")
        self.push_button_download_data.setEnabled(True)
        self.radioButton_2.setDisabled(False)

    def start_download_data(self):
        self.push_button_download_data.setText("Trwa pobieranie danych. \n Średni czas < 10s.")
        self.push_button_download_data.setEnabled(False)
        worker = DataWorker()
        worker.signals.result.connect(self.generate_station_view)
        worker.signals.finished.connect(self.update_ui_after_data_finished)
        self.thread_pool.start(worker)


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(list)


class DataWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(DataWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        data = DataManager(DbManager()).prepare_necessary_data()
        self.signals.result.emit(data)
        self.signals.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    db = DbManager()
    data_manager = DataManager(db)
    ui = UiMainWindow(data_manager)
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
