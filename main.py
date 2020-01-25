from main_window import UiMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from data_manager import DataManager
from db_manager import DbManager, DbManagerError
import logging_setup
import sys

if __name__ == "__main__":
    """
    Runs main application.
    """
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    main_logger = logging_setup.get_logger("main_program")
    try:
        data_base = DbManager()
        data_manager = DataManager(data_base)
        ui = UiMainWindow(data_manager, main_logger)
        ui.setup_ui(main_window)
        main_window.show()
    except DbManagerError as e:
        main_logger.exception(e)

    sys.exit(app.exec_())
