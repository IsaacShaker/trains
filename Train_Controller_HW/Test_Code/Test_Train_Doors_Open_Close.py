##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#                   Test: Train Doors Openning/Closing                   #
# Note:                                                                  #
# Doors can only open when the actual velocity equals 0.                 #
#                                                                        #
##########################################################################
from Train_Controller_HW.TrainControllerHW import Train_Controller_HW_UI
from PyQt6.QtWidgets import QApplication
import sys
import time

class TestApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        
        #Launch Train Controller Hardware UI
        self.train_controller_hw = Train_Controller_HW_UI()
        self.train_controller_hw.show()

        #Setup required variables:
        self.train_controller_hw.set_commanded_velocity(self.train_controller_hw.mph_to_mps(30))
        self.train_controller_hw.set_actual_velocity(self.train_controller_hw.set_actual_velocity(0))
        self.train_controller_hw.set_seconds(0)

        print ("==================================================================================")
        print (f"Actual Velocity: {self.train_controller_hw.get_actual_velocity()} MPH")
        print (f"Seconds value of the door timer: {self.train_controller_hw.get_seconds()}")
        print (f"Left Doors Status: {self.train_controller_hw.get_left_door_state()}")
        print (f"Right Doors Status: {self.train_controller_hw.get_right_door_state()}")
        print ("Use Door buttons on Hardware to open doors")
        time.sleep(2)
        if self.train_controller_hw.get_left_door_state() == True or self.train_controller_hw.get_right_door_state() == True:
            print (f"Left Doors Status: {self.train_controller_hw.get_left_door_state()}")
            print (f"Right Doors Status: {self.train_controller_hw.get_right_door_state()}")
            print (f"Timer for the doors will be simulated to a have passed 60 seconds in 3...")
            time.sleep(1)
            print ("2")
            time.sleep(1)
            print ("1")
            time.sleep(1)
            self.train_controller_hw.set_seconds(61)
            print (f"Left Doors Status: {self.train_controller_hw.get_left_door_state()}")
            print (f"Right Doors Status: {self.train_controller_hw.get_right_door_state()}")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())