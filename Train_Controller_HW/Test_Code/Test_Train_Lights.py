##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#             Test: Train Inside and Outside Train Lights                #
# Note:                                                                  #
# In Auto Mode - The lights will automatically turn on when:             #
#  1) The time of day is between the range of 8 PM and 8 AM              #
#  2) The train enters a tunnel                                          #
# In Manual Mode -                                                       #
#  1) The driver presses the respective light button                     #
#  2) Will automattically turn on in a tunnel                            #
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
        self.train_controller_hw.get_manual_mode()
        tunnel_beacon_info = "T1"

        if self.train_controller_hw.get_manual_mode():
            print ("==================================================================================")
            print ("TRAIN IS IN MANUAL MODE")
            print ("Use Light Buttons on hardware to test lights")
            print (f"Inside Light State: {self.train_controller_hw.get_inside_light_state}")
            print (f"Outside Light State: {self.train_controller_hw.get_outside_light_state}")
            print ("==================================================================================")
        else:
            print ("==================================================================================")
            print ("TRAIN IS IN MANUAL MODE")
            print ("Time of day set to 6 AM")
            self.train_controller_hw.set_hour(6)
            print (f"Inside Light State: {self.train_controller_hw.get_inside_light_state}")
            print (f"Outside Light State: {self.train_controller_hw.get_outside_light_state}")
            print ("In 5 seconds the time will change to 12 PM")
            time.sleep(5)
            self.train_controller_hw.set_hour(12)
            print (f"Inside Light State: {self.train_controller_hw.get_inside_light_state}")
            print (f"Outside Light State: {self.train_controller_hw.get_outside_light_state}")
            print ("In 5 seconds the Train will enter a tunnel")
            time.sleep(5)
            self.train_controller_hw.set_beacon_information(tunnel_beacon_info)
            print (f"Inside Light State: {self.train_controller_hw.get_inside_light_state}")
            print (f"Outside Light State: {self.train_controller_hw.get_outside_light_state}")
            print ("==================================================================================")
        print ("")
        print (f"")



        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())