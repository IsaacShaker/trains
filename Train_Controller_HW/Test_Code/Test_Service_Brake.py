########################################################################
#                   TRAIN CONTROLLER TEST CODE (HW)                    #
#                    Test Service Brake Activation                     #
# Note:                                                                #
# IF AND ONLY IF EMERGENCY BRAKE IS NOT ACTIVE                         #
# **In Auto Mode, Service brake is active when: **                     #
#  1) Actual speed is > commanded speed                                #
#  2) Calculation in order to use brakes to stop at a station is true  #
# **In Manual Mode, Service brake is active when: **                   #
#  1) Driver holds the service brake button                            #
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

        #Display Status of service brake and the affected variables:
        print ("==================================================================================")
        if self.train_controller_hw.get_emergency_brake_state:
            print (f"Service Brake Status is INNACTIVE because Emergency Brake is ACTIVE") 
        else: 
            if self.train_controller_hw.get_service_brake_state:
                print (f"Service Brake Status: ACTIVE") 
            else:
                print (f"Service Brake Status: INNACTIVE") 
        
        print (f"Actual Velocity: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_actual_velocity)} MPH")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())