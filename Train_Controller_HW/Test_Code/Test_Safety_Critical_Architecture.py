##########################################################################
#                    TRAIN CONTROLLER TEST CODE (HW)                     #
#                   Test: Safety Critical Architecture                   #
# Things to test:                                                        #
#  1) Doors cannot open when train is moving                             #
#  2) Emergency Brake can always be pressed                              #
#  3) Emergency Brake cannot be deactivated until train is stopped and   #
#     all Failure modes are not active                                   #
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

        #Test Emergency Brake Safety
        self.train_controller_hw.set_actual_velocity(20)
        self.train_controller_hw.set_emergency_brake_state(1)
        self.train_controller_hw.set_signal_failure(1)
        self.train_controller_hw.get_emergency_brake_state()
        self.train_controller_hw.set_signal_failure(0)
        self.train_controller_hw.set_emergency_brake_state(0)

        #Test Doors
        self.train_controller_hw.get_left_door_state()
        self.train_controller_hw.get_right_door_state()

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())