import time
import sys
from threading import Thread
# requests
from Test_UI import Train_Controller_SW_UI
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

        self.train_controller_sw.add_train()
        

        #all units are set in meters or m/s but displayed in feet or MPH
        self.train_controller_sw.train_list[0].set_authority(100)
        self.train_controller_sw.train_list[0].set_k_p(7000)
        self.train_controller_sw.train_list[0].set_k_i(20)
        self.train_controller_sw.train_list[0].set_commanded_velocity(10)

        #Regulate Train Speed at velocity setpoint from CTC & Train Drive
        self.train_controller_sw.train_list[0].set_commanded_velocity(10)

        #Set internal temperature setpoint
        self.train_controller_sw.train_list[0].set_temperature(66)

        #Emergency brake activation by driver
        self.train_controller_sw.train_list[0].set_k_p(7000)
        self.train_controller_sw.train_list[0].set_k_i(20)
        #self.train_controller_sw.train_list[0].set_e_brake(True)


        #Driver increases speed
        self.train_controller_sw.train_list[0].set_commanded_velocity(10)
        self.train_controller_sw.train_list[0].set_setpoint_velocity(5)

        #Driver decereases speed
        self.train_controller_sw.train_list[0].set_actual_velocity(10)
        self.train_controller_sw.train_list[0].set_setpoint_velocity(5)

        #Train lights on and off
        self.train_controller_sw.train_list[0].set_i_light(True)
        self.train_controller_sw.train_list[0].set_o_light(True)

        #Doors open at station
        self.train_controller_sw.train_list[0].set_authority(0)
        self.train_controller_sw.train_list[0].set_beacon_info("b3,3,Dormont")
        self.train_controller_sw.train_list[0].set_actual_velocity(0)

        

        





    
if __name__ == "__main__":
    # Initialize and run the application
    app = MainApp(sys.argv)
    sys.exit(app.exec())




