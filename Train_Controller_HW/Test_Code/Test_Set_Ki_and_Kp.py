########################################################################
#                  TRAIN CONTROLLER TEST CODE (HW)                     #
#                   Test Setting Ki and Kp Values                      #
#    Note: Ki and Kp Values can be set/reset at any point in the trip. #
#          Also, for HW implementation, changing ki and kp values via  #
#          this test code will work functionally in the backend but    #
#          will not display updated ki/kp values on the physical       #
#          hardware as the serial communication does not send those    #
#          values back to the arduino                                  #
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

        #Needed variables to show a change in power upon new ki and kp values:
        self.train_controller_hw.set_commanded_authority(500)
        self.train_controller_hw.set_commanded_velocity(20)
        self.train_controller_hw.set_actual_velocity(13)
        self.train_controller_hw.set_setpoint_velocity(15)

        #Display Updated values of Ki and Kp and the affected variables:
        print ("==================================================================================")
        self.train_controller_hw.set_ki_value(60000)
        self.train_controller_hw.set_ki_value(600)
        print (f"Current Ki Value: {self.train_controller_hw.get_ki_value}")
        print (f"Current Kp Value: {self.train_controller_hw.get_kp_value}")
        print (f"Current Commanded Power: {self.train_controller_hw.get_commanded_power} Watts")
        print ("==================================================================================")
        

        '''
        print (f"Current Ki Value: {self.train_controller_hw.get_ki_value}")
        new_ki = float(input("Input new Ki Value: "))
        self.train_controller_hw.set_ki_value(new_ki)
        print (f"Value of Ki from ")
        print (f"Current Ki Value: {self.train_controller_hw.get_ki_value}")
        new_ki = float(input("Input new Ki Value: "))
        self.train_controller_hw.set_ki_value(new_ki)
        print (f"Actual Velocity: {self.train_controller_hw.mps_to_mph(self.train_controller_hw.get_actual_velocity)} MPH")
        print ("==================================================================================")
        '''

        
        

if __name__ == "__main__":
    app = TestApp(sys.argv)
    sys.exit(app.exec())