import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt6.QtCore import QTimer
import requests
import serial

URL = 'http://127.0.0.1:5000'

class TrainControllerHardwareUI(QMainWindow):
    def __init__(self):
        super().__init__()

        #Required information for pyserial to read from arduino
        self.serial_port = "COM3" 
        self.baud_rate = 9600
        self.ser = None

        self.init_ui()
        self.open_serial_port()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)
        if self.ser and self.ser.is_open:  # Ensure the connection is open
            self.timer.timeout.connect(self.write_to_serial)
        self.timer.start(100)  # Read and write every 100ms

##############################################################################################
        #CLASS VARIABLES 
##############################################################################################
        #Data to read from arduino
        self.commanded_temperature = 70
        self.brake_state = 0
        self.light_state = 0
        self.door_state = 0
        self.commanded_power = 0

        #Data to be sent to train model (converting state variables to individual bools)
        self.emergency_brake_state = False
        self.service_brake_state = False
        self.inside_light = False
        self.outside_light = False
        self.left_door = False
        self.right_door = False

        #Data to write to Arduino
        self.required_doors = 0
        self.hour = 0
        self.seconds = 0
        self.brake_failure = False
        self.engine_failure = False
        self.signal_failure = False
        self.authority = 0
        self.actual_velocity = 0
        self.commanded_velocity = 0
        self.beacon_info = ""
        self.pa_announcement = ""
        self.beacon_identifier = ""
        self.at_stop = 0
        self.train_id = 0

        #Output dictionaries
        self.commanded_power_dict = {
            "commanded_power": self.commanded_power,
            "train_id": self.train_id
        }

        self.pa_announcement_dict = {
            "pa_announcement": self.pa_announcement,
            "train_id": self.train_id
        }

        self.temperature_dict = {
            "temperature": self.commanded_temperature,
            "train_id": self.train_id
        }

        self.lights_dict = {
            "o_light": self.outside_light,
            "i_light": self.inside_light,
            "train_id": self.train_id
        }

        self.doors_dict = {
            "l_door": self.left_door,
            "r_door": self.right_door,
            "train_id": self.train_id
        }

        self.brakes_dict = {
            "s_brake": self.service_brake_state,
            "e_brake": self.emergency_brake_state,
            "train_id": self.train_id
        }

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle("Train Controller Hardware")
        self.setGeometry(100, 100, 300, 200)

        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()

        # COM Port Input
        self.com_label = QLabel("COM Port:")
        self.com_input = QLineEdit()
        self.com_input.setPlaceholderText("e.g., COM3")
        layout.addWidget(self.com_label)
        layout.addWidget(self.com_input)

        # Baud Rate Input
        self.baud_label = QLabel("Baud Rate:")
        self.baud_input = QLineEdit()
        self.baud_input.setPlaceholderText("e.g., 9600")
        layout.addWidget(self.baud_label)
        layout.addWidget(self.baud_input)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.open_serial_port)
        layout.addWidget(self.connect_button)

        # Status Label
        self.status_label = QLabel("Arduino Status: Not Connected")
        layout.addWidget(self.status_label)

        # Set layout
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


    def open_serial_port(self):
        if self.com_input.text():
            self.serial_port = self.com_input.text()
        else:
            self.serial_port = "COM3"
        if self.baud_input.text():
            self.baud_rate = self.baud_input.text()
        else: 
            self.baud_rate = 9600

        try:
            # Attempt to open serial connection
            self.ser = serial.Serial(self.serial_port, int(self.baud_rate), timeout=1)
            if self.ser.is_open:
                self.status_label.setText("Arduino Status: Connected")
        except (serial.SerialException, ValueError):
            self.status_label.setText("Arduino Status: Not Connected")

    def read_serial(self):
        if self.ser and self.ser.in_waiting > 0:
            # Read a line from the serial connection
            line = self.ser.readline().decode().strip()

            #Split the comma-separated values
            #Line comes in the form of "commanded_temperature, brake_state, door_state, light_state, commanded_power"
            if line:
                values = line.split(',')
                if len(values) == 6:  # Ensure we have 6 values
                    self.set_commanded_temperature(values[0])
                    #self.setpoint_velocity.setText(f"Setpoint Velocity: {values[1]} mph")
                    self.set_brake_state(values[2])
                    self.set_door_state(values[3])
                    self.set_light_state(values[4])
                    self.set_commanded_power(values[5])

    def write_to_serial(self):
        self.decode_beacon_info(self.beacon_info)
        #Continuously send backend variables to the serial port.
        #Create the command string using individual getter functions
        command = (         
            str(self.get_hour()) + "," + 
            str(self.get_seconds()) + "," + 
            str(self.get_brake_failure()) + "," +
            str(self.get_engine_failure()) + "," +
            str(self.get_signal_failure()) + "," +
            str(self.get_authority()) + "," +
            str(self.get_actual_velocity()) + "," +
            str(self.get_commanded_velocity()) + "," +
            self.get_pa_announcement() + "," +
            str(self.get_required_doors()) + "\n" 
        )
        self.ser.write(command.encode())

    def decode_beacon_info(self, encoded_beacon_info):
        if encoded_beacon_info:
            values = encoded_beacon_info.split(',')
            #Assign variables for the case of a beacon at a station
            if len(values) == 3:  
                self.set_beacon_identifier(values[0])
                self.set_required_doors(values[1])
                self.set_pa_announcement(values[2])
                self.set_at_stop(1)
            else:
                self.set_beacon_identifier("")
                self.set_at_stop(0)
                self.set_required_doors(0)
                self.set_pa_announcement("")




#Set Functions:
#========================================================
    def set_inside_light_state(self, input):
        self.inside_light = input
        self.lights_dict["i_light"] = self.inside_light
        
    def set_outside_light_state(self, input):
        self.outside_light = input
        self.lights_dict["o_light"] = self.outside_light
    
    def set_emergency_brake_state(self, input):
        self.emergency_brake_state = input
        self.brakes_dict["e_brake"] = self.emergency_brake_state
    
    def set_service_brake_state(self, input):
        self.service_brake_state = input
        self.brakes_dict["s_brake"] = self.service_brake_state

    def set_left_door_state(self, input):
        self.left_door_state = input
        self.doors_dict["l_door"] = self.left_door_state

    def set_right_door_state(self, input):
        self.right_door_state = input
        self.doors_dict["r_door"] = self.right_door_state

    def set_commanded_temperature(self, input):
        self.commanded_temperature = input
        self.temperature_dict["temperature"] = self.commanded_temperature

    def set_brake_state(self, input):
        self.brake_state = input

        if(self.brake_state == 0): #no brakes requested
            self.set_emergency_brake_state(False)
            self.set_service_brake_state(False)
        elif(self.brake_state == 1): #e brake requested
            self.set_emergency_brake_state(True)
            self.set_service_brake_state(False)
        elif(self.brake_state == 2): #service brake requested
            self.set_emergency_brake_state(False)
            self.set_service_brake_state(True)

    def set_light_state(self, input):
        self.light_state = input
        
        if(self.light_state == 0): #no lights requested
            self.set_inside_light_state(False)
            self.set_outside_light_state(False)
        elif(self.light_state == 1): #outside light only
            self.set_inside_light_state(False)
            self.set_outside_light_state(True)
        elif(self.light_state == 2): #inside light only
            self.set_inside_light_state(True)
            self.set_outside_light_state(False)
        elif(self.light_state == 3): #both lights requested
            self.set_inside_light_state(True)
            self.set_outside_light_state(True)
        
    def set_door_state(self, input):
        self.door_state = input

        if(self.door_state == 0):   #no doors
            self.set_left_door_state(False)
            self.set_right_door_state(False)
        elif(self.door_state == 1): #right door only
            self.set_left_door_state(False)
            self.set_right_door_state(True)
        elif(self.door_state == 2): #left door only
            self.set_left_door_state(True)
            self.set_right_door_state(False)
        elif(self.door_state == 3): #both doors
            self.set_left_door_state(True)
            self.set_right_door_state(True)

    def set_commanded_power(self, input):
        self.commanded_power = input
        self.commanded_power_dict["commanded_power"] = self.commanded_power

    def set_required_doors(self, input):
        self.required_doors = input
    
    def set_hour(self, input):
        self.hour = input
    
    def set_seconds(self, input):
        self.seconds = input

    def set_brake_failure(self, input):
        self.brake_failure = input
    
    def set_engine_failure(self, input):
        self.engine_failure = input

    def set_signal_failure(self, input):
        self.signal_failure = input

    def set_authority(self, input):
        self.authority = input

    def set_actual_velocity(self, input):
        self.actual_velocity = input

    def set_commanded_velocity(self, input):
        self.commanded_velocity = input

    def set_beacon_information(self, input):
        self.beacon_information = input
        self.decode_beacon_info(self.beacon_information)

    def set_beacon_identifier(self, input):
        self.beacon_identifier = input  

    def set_pa_announcement(self, input):
        self.pa_announcement = input    
        self.pa_announcement_dict["pa_announcement"] = self.pa_announcement

    def set_at_stop(self, input):
        self.at_stop = input


#Get Functions:
#========================================================
    def get_inside_light_state(self):
        return self.inside_light
        
    def get_outside_light_state(self):
        return self.outside_light 
    
    def get_emergency_brake_state(self):
        return self.emergency_brake_state
    
    def get_service_brake_state(self):
        return self.service_brake_state 

    def get_left_door_state(self):
        return self.left_door_state 

    def get_right_door_state(self):
        return self.right_door_state 

    def get_commanded_temperature(self):
        return self.commanded_temperature 

    def get_brake_state(self):
        return self.brake_state 

    def get_light_state(self):
        return self.light_state 
        
    def get_door_state(self):
        return self.door_state

    def get_comanded_power(self):
        return self.commanded_power 

    def get_required_doors(self):
        return self.required_doors 
    
    def get_hour(self):
        return self.hour 
    
    def get_seconds(self):
        return self.seconds 

    def get_brake_failure(self):
        return self.brake_failure 
    
    def get_engine_failure(self):
        return self.engine_failure

    def get_signal_failure(self):
        return self.signal_failure 

    def get_authority(self):
        return self.authority

    def get_actual_velocity(self):
        return self.actual_velocity 

    def get_commanded_velocity(self):
        return self.commanded_velocity

    def get_beacon_information(self):
        return self.beacon_information
    
    def get_pa_announcement(self):
        return self.pa_announcement

    def get_beacon_identifier(self):
        return self.beacon_identifier

    def get_at_stop(self):
        return self.at_stop
    
    def get_train_id(self):
        return self.train_id
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainControllerHardwareUI()
    window.show()
    sys.exit(app.exec())