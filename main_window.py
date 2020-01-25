from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from data_manager import DataManager, DataManagerError
from db_manager import DbManager
from graph_drawer import GraphDrawer
from collections import defaultdict
from logging_setup import get_logger
import logging


class UiMainWindow:
    MODE_STATION = 0
    MODE_SENSOR = 1

    def __init__(self, d_manager: DataManager, logger: logging.Logger):
        self.thread_pool = QThreadPool()
        self.data_manager = d_manager
        self.selected_sensors = defaultdict(set)
        self.selected_stations = defaultdict(set)
        self.mode = self.MODE_STATION
        self.station_data = None
        self.current_param = None
        self.current_station = None
        self.logger = logger

    def setup_ui(self, main_window):
        """Generates UI"""
        main_window.setObjectName("MainWindow")
        main_window.resize(1000, 713)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.central_widget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 900, 391))
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

        self.params_widget = QtWidgets.QTableWidget(self.central_widget)
        self.params_widget.setGeometry(QtCore.QRect(10, 420, 361, 231))
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

        self.main_label = QLabel(self.central_widget)
        self.main_label.setGeometry(QtCore.QRect(10, 400, 500, 16))
        self.main_label.setObjectName("main_label")

        self.push_button_draw_graph = QPushButton(self.central_widget)
        self.push_button_draw_graph.setGeometry(QtCore.QRect(10, 660, 171, 23))
        self.push_button_draw_graph.setObjectName("push_button_draw_graph")
        self.push_button_draw_graph.clicked.connect(lambda: self.download_data(True))
        self.push_button_draw_graph.setDisabled(True)

        self.push_button_download_specific_data = QPushButton(self.central_widget)
        self.push_button_download_specific_data.setGeometry(QtCore.QRect(200, 660, 171, 23))
        self.push_button_download_specific_data.setObjectName("push_button_download_specific_data")
        self.push_button_download_specific_data.clicked.connect(lambda: self.download_data(False))
        self.push_button_download_specific_data.setDisabled(True)

        self.push_button_download_data = QPushButton(self.central_widget)
        self.push_button_download_data.setGeometry(QtCore.QRect(450, 450, 141, 61))
        self.push_button_download_data.setObjectName("push_button_download_data")
        self.push_button_download_data.clicked.connect(self.start_download_data)

        self.push_button_clear_cache = QPushButton(self.central_widget)
        self.push_button_clear_cache.setGeometry(QtCore.QRect(450, 520, 141, 61))
        self.push_button_clear_cache.setObjectName("push_button_clear_cache")
        self.push_button_clear_cache.clicked.connect(self.clear_cache)

        self.push_button_select_all = QPushButton(self.central_widget)
        self.push_button_select_all.setGeometry(QtCore.QRect(600, 450, 141, 61))
        self.push_button_select_all.setObjectName("push_button_select_all")
        self.push_button_select_all.clicked.connect(lambda: self.toggle_all_checkboxes(True))

        self.push_button_deselect_all = QPushButton(self.central_widget)
        self.push_button_deselect_all.setGeometry(QtCore.QRect(600, 520, 141, 61))
        self.push_button_deselect_all.setObjectName("push_button_deselect_all")
        self.push_button_deselect_all.clicked.connect(lambda: self.toggle_all_checkboxes(False))

        self.layout_widget_radio_buttons = QtWidgets.QWidget(self.central_widget)
        self.layout_widget_radio_buttons.setGeometry(QtCore.QRect(460, 590, 160, 61))
        self.layout_widget_radio_buttons.setObjectName("layout_widget_radio_buttons")

        self.layout_radio_buttons = QtWidgets.QVBoxLayout(self.layout_widget_radio_buttons)
        self.layout_radio_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout_radio_buttons.setObjectName("layout_radio_buttons")

        self.radio_button_station_mode = QtWidgets.QRadioButton(self.layout_widget_radio_buttons)
        self.radio_button_station_mode.setObjectName("radio_button_station_mode")
        self.layout_radio_buttons.addWidget(self.radio_button_station_mode)
        self.radio_button_station_mode.setChecked(True)
        self.radio_button_station_mode.toggled.connect(self.radio_button_on_click)

        self.radio_button_sensor_mode = QtWidgets.QRadioButton(self.layout_widget_radio_buttons)
        self.radio_button_sensor_mode.setObjectName("radio_button_sensor_mode")
        self.layout_radio_buttons.addWidget(self.radio_button_sensor_mode)
        self.radio_button_sensor_mode.setDisabled(True)

        main_window.setCentralWidget(self.central_widget)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("statusbar")
        main_window.setStatusBar(self.status_bar)

        self.re_translate_ui(main_window)
        self.radio_button_on_click()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        """Adds all labels for items"""
        _t = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_t("MainWindow", "Klient jakości powietrza"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_t("MainWindow", "Nazwa stacji"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_t("MainWindow", "Długość geo."))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_t("MainWindow", "Szerokość geo."))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_t("MainWindow", "Miasto"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_t("MainWindow", "Adres"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_t("MainWindow", "Województwo"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_t("MainWindow", "Użyj"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_t("MainWindow", "Id"))
        # __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        # self.tableWidget.setSortingEnabled(__sortingEnabled)
        item = self.params_widget.horizontalHeaderItem(0)
        item.setText(_t("MainWindow", "Użyj"))
        item = self.params_widget.horizontalHeaderItem(1)
        item.setText(_t("MainWindow", "Nazwa"))
        item = self.params_widget.horizontalHeaderItem(2)
        item.setText(_t("MainWindow", "Symbol"))
        self.main_label.setText(_t("MainWindow", "Stanowiska pomiarowe dla wybranej stacji"))
        self.push_button_draw_graph.setText(_t("MainWindow", "Rysuj wykres dla stacji"))
        self.push_button_download_data.setText(_t("MainWindow", "Pobierz dane"))
        self.push_button_clear_cache.setText(_t("MainWindow", "Usuń historię zapytań"))
        self.radio_button_station_mode.setText(_t("MainWindow", "Tryb jednej stacji"))
        self.radio_button_sensor_mode.setText(_t("MainWindow", "Tryb jednego stanowiska"))
        self.push_button_download_specific_data.setText(_t("MainWindow", "Pobierz wybrane dane"))
        self.push_button_select_all.setText(_t("MainWindow", "Zaznacz wszystko"))
        self.push_button_deselect_all.setText(_t("MainWindow", "Odznacz wszystko"))

    @staticmethod
    def add_checkbox_to_table(table: QTableWidget, row, col, checked=False):
        """Adds checkboxes to given table by row, col"""
        check_box_item = QtWidgets.QTableWidgetItem()
        check_box_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if checked:
            check_box_item.setCheckState(QtCore.Qt.Checked)
        else:
            check_box_item.setCheckState(QtCore.Qt.Unchecked)
        table.setItem(row, col, check_box_item)

    def clear_cache(self):
        """Clears all cache callback"""
        try:
            self.data_manager.delete_cache()
        except DataManagerError as e:
            self.logger.exception(e)
            self.show_exception_box(e)

    def enable_push_buttons(self):
        """Helper method for enabling download data buttons"""
        enable = False
        if self.mode == self.MODE_STATION:
            if self.current_station and self.selected_sensors[self.current_station]:
                enable = True
        else:
            if self.current_param and self.selected_stations[self.current_param]:
                enable = True

        self.push_button_draw_graph.setEnabled(enable)
        self.push_button_download_specific_data.setEnabled(enable)

    def toggle_all_checkboxes(self, select=True):
        """Callback method for selecting all checkboxes."""

        if self.mode == self.MODE_STATION:
            for row in range(self.params_widget.rowCount()):
                self.add_checkbox_to_table(self.params_widget, row, 0, select)
                if select:
                    self.selected_sensors[self.current_station].add(int(self.params_widget.item(row, 3).text()))
                else:
                    self.selected_sensors[self.current_station] = set()
        else:
            for row in range(self.tableWidget.rowCount()):
                self.add_checkbox_to_table(self.tableWidget, row, 6, select)
                if select:
                    self.selected_stations[self.current_param].add(int(self.tableWidget.item(row, 7).text()))
                else:
                    self.selected_stations[self.current_param] = set()
        self.enable_push_buttons()

    def download_data(self, draw_graph=True):
        """
        Download data callback. Gets data from API/Db

        :param draw_graph: Bool
        """
        if self.mode == self.MODE_STATION:
            sensors = self.selected_sensors[self.current_station]
            try:
                data = self.data_manager.get_data_by_sensor_ids_for_graphing(sensors)
                if draw_graph:
                    station_name = self.data_manager.get_station_name_by_id(self.current_station)
                    GraphDrawer.draw_station_graph(station_name, data)
            except DataManagerError as e:
                self.logger.exception(e)
                self.show_exception_box(e)
        else:
            stations = self.selected_stations[self.current_param]
            try:
                data = self.data_manager.get_data_by_station_ids_for_graphing(stations, self.current_param)
            except DataManagerError as e:
                self.logger.exception(e)
                self.show_exception_box(e)
            if draw_graph:
                GraphDrawer.draw_sensor_graph(self.current_param, data)

    def generate_station_view(self, stations=None):
        """
        Generates station view from specified data
        :type stations: list
        """
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
        """
        Callback for main table item clicked
        :param item: QWidgetItem
        """
        item_row = item.row()
        station_id = int(self.tableWidget.item(item_row, 7).text())
        if self.mode == self.MODE_STATION:
            try:
                data = self.data_manager.get_sensors(int(station_id))
            except DataManagerError as e:
                self.logger.exception(e)
                self.show_exception_box(e)
            self.current_station = station_id
            self.generate_sensor_table_view(data)
        else:
            if item.checkState() == QtCore.Qt.Checked:
                self.selected_stations[self.current_param].add(station_id)
            elif item.checkState is not QtCore.Qt.Unchecked and item.column() == 6:
                self.selected_stations[self.current_param].discard(station_id)

        self.enable_push_buttons()

    def generate_sensor_table_view(self, data):
        """
        Generates sensor table view from given data
        :param data: list
        """
        self.params_widget.setRowCount(len(data))
        for row, sensor in enumerate(data):
            if self.mode == self.MODE_STATION:
                checked = True if sensor[2] in self.selected_sensors[self.current_station] else False
                self.add_checkbox_to_table(self.params_widget, row, 0, checked)
            for column, element in enumerate(sensor):
                column += 1
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setText(str(element))
                self.params_widget.setItem(row, column, item)
        self.params_widget.itemClicked.connect(self.handle_sensor_table_item_clicked)

    def handle_sensor_table_item_clicked(self, item):
        """
        Handles click event for sensor table widget.
        :param item: QCheckBox
        """
        if self.mode == self.MODE_STATION:
            sensor_id = int(self.params_widget.item(item.row(), 3).text())
            if item.checkState() == QtCore.Qt.Checked and item.column() == 0:
                self.selected_sensors[self.current_station].add(sensor_id)
            elif item.checkState is not QtCore.Qt.Unchecked and item.column() == 0:
                self.selected_sensors[self.current_station].discard(sensor_id)
        else:
            param_code = self.params_widget.item(item.row(), 2).text()
            self.current_param = param_code
            try:
                data = self.data_manager.get_all_stations_by_param(param_code)
            except DataManagerError as e:
                self.logger.exception(e)
                self.show_exception_box(e)
            self.generate_station_view(data)
        self.enable_push_buttons()

    def radio_button_on_click(self):
        """Callback for changing mode"""
        self.current_param = None
        self.current_station = None
        if self.radio_button_station_mode.isChecked():
            self.mode = self.MODE_STATION
            self.tableWidget.setColumnHidden(6, True)
            self.main_label.setText("Tryb jednej stacji. Poniżej znajduje się lista dostępnych stanowisk pomiarowych: ")
            self.push_button_draw_graph.setText("Rysuj wykres dla stacji")
            self.params_widget.setRowCount(0)
            self.params_widget.setColumnHidden(0, False)
            if self.station_data:
                self.generate_station_view(self.station_data)
        else:
            if self.station_data is None:
                self.radio_button_sensor_mode.toggle()
                self.radio_button_station_mode.toggle()
            self.mode = self.MODE_SENSOR
            self.main_label.setText("Tryb jednego stanowiska pomiarowego. Proszę wybrać stacje pomiarowe (limit: 20)")
            self.push_button_draw_graph.setText("Rysuj wykres dla stanowiska")
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnHidden(6, False)
            self.params_widget.setColumnHidden(0, True)

            try:
                data = self.data_manager.get_all_sensors_for_view()
                self.generate_sensor_table_view(data)
            except DataManagerError as e:
                self.logger.exception(e)
                self.show_exception_box(e)
        self.enable_push_buttons()

    def update_ui_after_data_download_finished(self):
        """Updates ui after main data download is finished"""
        self.push_button_download_data.setText("Pobierz dane")
        self.push_button_download_data.setEnabled(True)
        self.push_button_clear_cache.setEnabled(True)
        self.radio_button_sensor_mode.setDisabled(False)

    def start_download_data(self):
        """ Starts downloading data"""
        self.push_button_download_data.setText("Trwa pobieranie danych.\nŚredni czas < 10s.")
        self.push_button_download_data.setEnabled(False)
        self.push_button_clear_cache.setEnabled(False)
        worker = ApiDataWorker()
        worker.signals.result.connect(self.generate_station_view)
        worker.signals.error.connect(self.show_exception_box)
        worker.signals.finished.connect(self.update_ui_after_data_download_finished)
        self.thread_pool.start(worker)

    @staticmethod
    def show_exception_box(exception_message):
        """
        Show message box with exception info.
        :param exception_message: Exception
        """
        msg = QMessageBox()
        msg.setWindowTitle("Błąd!")
        msg.setText(str(exception_message))
        msg.setIcon(QMessageBox.Critical)
        res = msg.exec_()


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(list)
    error = pyqtSignal(Exception)


class ApiDataWorker(QRunnable):

    def __init__(self, *args, **kwargs):
        super(ApiDataWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            data = DataManager(DbManager()).prepare_necessary_data()
            self.signals.result.emit(data)
        except DataManagerError as e:
            self.signals.error.emit(e)
            get_logger("main_program").exception(e)
        finally:
            self.signals.finished.emit()
