##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#              Test: Using Speed and Authority from circuit              #
# Note:                                                                  #
# Commanded speed can be changed on any block though by our groups       #
# implementation, even if a new authority is sent out the train          #
# controller will not update the value until the previous authority has  #
# been reached                                                           #
#                                                                        #
##########################################################################
from Train_Controller_HW.TrainControllerHW import Train_Controller_HW_UI
from PyQt6.QtWidgets import QApplication
import sys

class TestApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        #Launch Train Controller Hardware UI
        self.train_controller_hw = Train_Controller_HW_UI()
        self.train_controller_hw.show()

        #Setup required variables:
        self.train_controller_hw.set_commanded_velocity(self.train_controller_hw.mph_to_mps(30))
        self.speed_mph = 0

        #Display Status of emergency brake and the affected variables:
        print ("==================================================================================")
        print (f"Receive 500 meters authority from track circuit, followed by 300 meters")
        self.train_controller_hw.set_commanded_authority(500)
        self.train_controller_hw.set_commanded_authority(300)
        print (f"Current Authority value: {self.train_controller_hw.get_current_authority} Feet")
        print (f"Commanded Authority value: {self.train_controller_hw.get_commanded_authority} Feet")
        print (f"Receive a commanded velocity of 43.5 MPH")
        self.train_controller_hw.set_commanded_velocity(19.44624) # in meters per second
        print (f"Commanded Speed: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_commanded_velocity)} MPH")
        print (f"Receive a commanded velocity of 20 MPH")
        self.train_controller_hw.set_commanded_velocity(8.9408) # in meters per second
        print (f"Commanded Speed: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_commanded_velocity)} MPH")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())