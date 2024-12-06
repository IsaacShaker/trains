########################################################################
#                   TRAIN CONTROLLER TEST CODE (HW)                    #
#                Test Setting the Internal Temperature                 #
#                Note: Manual Mode - Set by Driver                     #
#                      Auto Mode   - Always equal to 68 Degrees F      #
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

        #Display Set Temperature for respective mode (Manual or Auto):
        if self.train_controller_hw.get_manual_mode():
            print (f"Manual Mode Set Temperature: {self.train_controller_hw.get_commanded_temperature}")
        else:
            print (f"Auto Mode Set Temperature: {self.train_controller_hw.get_commanded_temperature}")

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())