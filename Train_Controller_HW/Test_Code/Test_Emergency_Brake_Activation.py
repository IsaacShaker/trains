########################################################################
#                  TRAIN CONTROLLER TEST CODE (HW)                     #
#                  Test Emergency Brake Activation                     #
#    Note: Emergency Brake can be pressed at anytime by the driver     #
#                                                                      #
########################################################################
from Train_Controller_HW.TrainControllerHW import Train_Controller_HW_UI
from PyQt6.QtWidgets import QApplication
import sys

class TestApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        #Launch Train Controller Hardware UI
        self.train_controller_hw = Train_Controller_HW_UI()
        self.train_controller_hw.show()

        #Display Status of emergency brake and the affected variables:
        print ("==================================================================================")
        if self.train_controller_hw.get_emergency_brake_state:
            print (f"Emergency Brake Status: ACTIVE") 
        else: 
            print (f"Emergency Brake Status: INNACTIVE") 
        
        print (f"Actual Velocity: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_actual_velocity)} MPH")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())