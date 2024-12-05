import time
import sys
from threading import Thread
import requests
from User_Interface import Train_Controller_SW_UI
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QStackedLayout,
    QFrame,
    QTabWidget,
    QStackedWidget,
)

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.train_controller_sw = Train_Controller_SW_UI()

        self.train_controller_sw.show()
        

        #all units are set in meters or m/s but displayed in feet or MPH
        self.train_controller_sw.train_list[0].set_authority(100)
        self.train_controller_sw.train_list[0].set_k_p(7000)
        self.train_controller_sw.train_list[0].set_k_i(20)
        self.train_controller_sw.train_list[0].set_commanded_velocity(10)



    
if __name__ == "__main__":
    # Initialize and run the application
    app = MainApp(sys.argv)
    sys.exit(app.exec())




