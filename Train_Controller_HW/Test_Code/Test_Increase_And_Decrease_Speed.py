##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#                   Test: Increase and Decrease Speed                    #
# Note:                                                                  #
# SETPOINT VELOCIY CAN NEVER EXCEED COMMANDED VELOCITY                   #
# ALSO SETPOINT SPEED CANNOT BE INCREASED UNTIL AN AUTHORITY IS RECEIVED #
# - In Auto Mode, setpoint velocity matches commanded velocity           #
# - In Manual Mode, setpoint velocity is decided by driver's input       #
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
        self.train_controller_hw.set_commanded_authority(500)
        self.train_controller_hw.set_commanded_velocity(self.train_controller_hw.mph_to_mps(30))
        self.speed_mph = 0

        #Display Status of emergency brake and the affected variables:
        print ("==================================================================================")
        print (f"Commanded Speed: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_commanded_velocity)} MPH")
        print (f"Current Setpoint Velocity = {self.train_controller_hw.get_setpoint_velocity} MPH")
        print (f"Starting from 0 MPH attempt to increase Setpoint Velocity by 5 MPH to 43.5 MPH:")
        for x in range(0, 8, 1):
            self.speed_mph += 5
            self.train_controller_hw.set_setpoint_velocity(self.speed_mph)
            print (f"Setpoint Velocity Set to: {self.train_controller_hw.get_setpoint_velocity} MPH on iteration {x}")
        print (f"Starting from the current Setpoint speed of {self.train_controller_hw.get_setpoint_velocity}, decrease Setpoint Velocity by 5 MPH until 0 MPH is reached:")
        for x in range(0, 6, 1):
            self.speed_mph -= 5 
            self.train_controller_hw.set_setpoint_velocity(self.speed_mph)
            print (f"Setpoint Velocity Set to: {self.train_controller_hw.get_actual_velocity} MPH on iteration {x}")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())