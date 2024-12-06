##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#                    Test: Announcements at Stations                     #
# Note:                                                                  #
# Announcements are received by beacons, at the stops and sent to the    #
# train model when received                                              #
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
        self.train_controller_hw.set_beacon_information("B1,1,Inglewood")

        #Display Status of emergency brake and the affected variables:
        print ("==================================================================================")
        print (f"Inputted Beacon Info: 'B1,1,Inglewood'")
        print (f"PA announcement sent to Train Model: {self.train_controller_hw.get_pa_announcement}")
        print ("==================================================================================")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())