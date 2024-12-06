from Train_Controller_HW.TrainControllerHW import Train_Controller_HW_UI
from PyQt6.QtWidgets import QApplication
import sys


class TestApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        #Launch Train Controller Hardware UI
        self.train_controller_hw = Train_Controller_HW_UI()
        self.train_controller_hw.show()

        #Set necessary variables for test case:
        #Note: velocity is input to train controller as m/s but displayed in MPH
        self.train_controller_hw.set_commanded_velocity(19.45) #Roughly 43.5 MPH
        self.train_controller_hw.set_manual_mode(True) #Ensure train is in manual mode

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())