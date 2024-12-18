import sys
from PyQt6.QtWidgets import QApplication, QFrame, QGridLayout, QTabWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt6.QtCore import QTimer
import requests
import serial

URL = 'http://127.0.0.1:5000'

sim_speed = 10

class Train_Controller_HW_UI(QMainWindow):
    def __init__(self, model_list):
        super().__init__()

    #Required information for pyserial to read from arduino
        self.serial_port = "COM3" 
        self.baud_rate = 9600
        #self.serial_port = "" 
        #self.baud_rate = 0
        self.ser = None
        self.connection_status = "Not Connected"

        self.timer = QTimer(self)
        self.timer.setInterval(90) # Read every 90ms @ sim speed of 1
        self.timer.timeout.connect(self.controller_logic)
        self.timer.start()  
        
        self.init_ui()
        
        self.train_model_list = model_list

    ###################################
    #       CLASS VARIABLES           #
    ###################################
    #Data to read from arduino
        self.commanded_temperature = 68
        self.brake_state = 0
        self.light_state = 0
        self.door_state = 0
        self.commanded_power = 0.0
        self.left_door_request = False
        self.right_door_request = False
        self.first_time_opening_doors = True
        self.setpoint_velocity = 0.0
        self.ki_value = 0.0
        self.kp_value = 0.0

        self.ek_previous = 0.0
        self.ek_current = 0.0
        self.uk_previous = 0.0
        self.uk_current = 0.0

        self.current_beacon_identifier = ""
        self.previous_beacon_identifier = ""
        self.station_name = ""

        self.reset_left_door_timer = False
        self.reset_right_door_timer = False
        self.ARD_outside_light_request = False
        self.ARD_inside_light_request = False
        self.e_brake_state = False
        self.s_brake_state = False
        self.brake_warning = False

    #Data to be sent to train model (converting state variables to individual bools)
        self.emergency_brake_state = False
        self.service_brake_state = False
        self.inside_light = False
        self.outside_light = False
        self.left_door = False
        self.right_door = False
        self.pa_announcement = ""
        self.train_id = 0

    #Inputs from Train Model
        self.beacon_info = ""
        #Data to write to Arduino
        self.required_doors = 0
        self.hour = 0
        self.seconds = 0
        self.brake_failure = False
        self.engine_failure = False
        self.signal_failure = False
        self.commanded_authority = 0.0
        self.current_authority = 0.0
        self.actual_velocity = self.train_model_list[0].get_currentVelocity()
        self.commanded_velocity = 0.0
        self.beacon_identifier = ""
        self.at_stop = 0
        self.in_tunnel = False
        self.manual_mode = False
        self.difference_in_authority = 0.0
        self.counter_authority = 1
        self.train_instantion = True

    #Inputs from world clock class
        self.sim_speed = 1
    
    #Other Timing Variables
        self.T = .09 #* self.sim_speed #Represents the period at which current_authority and commanded_power are calculated - Changes in relation to clock speed
        self.counter = 1

    #Output dictionaries
        self.auth_diff_dict = {
            "auth_diff": self.current_authority,
            "train_id": 0
        }

        self.commanded_power_dict = {
            "commanded_power": self.commanded_power,
            "train_id": 0
        }

        self.pa_announcement_dict = {
            "pa_announcement": self.pa_announcement,
            "train_id": 0
        }

        self.temperature_dict = {
            "temperature": self.commanded_temperature,
            "train_id": 0
        }

        self.lights_dict = {
            "o_light": self.outside_light,
            "i_light": self.inside_light,
            "train_id": 0
        }

        self.doors_dict = {
            "l_door": self.left_door,
            "r_door": self.right_door,
            "train_id": 0
        }

        self.brakes_dict = {
            "s_brake": self.service_brake_state,
            "e_brake": self.emergency_brake_state,
            "train_id": 0
        }


#UI FUNCTIONS 
    def init_ui(self):
        # Set up main window properties
        #UI dimensions:
        self.total_width = 400
        self.total_height = 400
        self.setWindowTitle("Train Controller Hardware")
        self.setGeometry(100, 100, self.total_width, self.total_height) #pos, pos, width, height

        # Initialize the tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize "Home" tab
        self.home_tab = QWidget()
        self.init_home_tab()
        self.tabs.addTab(self.home_tab, "Home")

        # Initialize "Test Bench" tab
        self.test_bench_tab = QWidget()
        self.init_test_bench_tab()
        self.tabs.addTab(self.test_bench_tab, "Test Bench")

    def init_home_tab(self):
        # Set up the "Home" tab layout and widgets
        layout_home = QGridLayout()
        layout_title = QVBoxLayout()
        layout_input = QVBoxLayout()
        layout_status = QVBoxLayout()

        # Frames:
        frame_title = QFrame()
        frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        frame_title.setFrameShadow(QFrame.Shadow.Raised)
        frame_title.setStyleSheet("background-color: gray; border-radius: 20px;")
        frame_title.setLineWidth(3)
        frame_title.setFixedSize(self.total_width - 10,50)

        frame_input = QFrame()
        frame_input.setFrameShape(QFrame.Shape.StyledPanel)
        frame_input.setFrameShadow(QFrame.Shadow.Raised)
        frame_input.setStyleSheet("background-color: gray; border-radius: 20px;")
        frame_input.setLineWidth(3)
        frame_input.setFixedSize(self.total_width - 10,150)

        frame_status = QFrame()
        frame_status.setFrameShape(QFrame.Shape.StyledPanel)
        frame_status.setFrameShadow(QFrame.Shadow.Raised)
        frame_status.setStyleSheet("background-color: gray; border-radius: 20px;")
        frame_status.setLineWidth(3)
        frame_status.setFixedSize(self.total_width - 10,50)

        # COM Port Input
        line_layout_com = QHBoxLayout()
        self.com_label = QLabel("COM Port: ")
        self.com_input = QLineEdit()
        self.com_input.setPlaceholderText("e.g., COM3")
        line_layout_com.addWidget(self.com_label)
        line_layout_com.addWidget(self.com_input)

        # Baud Rate Input
        line_layout_baud = QHBoxLayout()
        self.baud_label = QLabel("Baud Rate:")
        self.baud_input = QLineEdit()
        self.baud_input.setPlaceholderText("e.g., 9600")
        line_layout_baud.addWidget(self.baud_label)
        line_layout_baud.addWidget(self.baud_input)

        # Connect Button
        line_layout_button = QHBoxLayout()
        self.connect_button = QPushButton("CONNECT")
        self.connect_button.setStyleSheet("background-color: #772CE8; border-radius: 5px;")
        self.connect_button.setFixedSize(self.total_width - 30,40)
        self.connect_button.clicked.connect(self.open_serial_port)
        line_layout_button.addWidget(self.connect_button)
        line_layout_button.addStretch()

        # Status Connection Row
        line_layout_connection_status = QHBoxLayout()
        self.arduino_connection_line = QLabel("Arduino Connection Status: ")
        self.connection_status = QLabel("Serial port not connected.")
        if self.connection_status.text() == "Serial port opened successfully.":
            self.connection_status.setStyleSheet("color: green;")
        else:
            self.connection_status.setStyleSheet("color: red;")
        line_layout_connection_status.addWidget(self.arduino_connection_line)
        line_layout_connection_status.addWidget(self.connection_status)
        

        # Set layout to the home tab
        layout_title.addLayout(self.create_header("TRAIN CONTROLLER HARDWARE", 15))
        layout_input.addLayout(line_layout_com)
        layout_input.addLayout(line_layout_baud)
        layout_input.addLayout(line_layout_button)
        layout_status.addLayout(line_layout_connection_status)
        
        frame_title.setLayout(layout_title)
        frame_input.setLayout(layout_input)
        frame_status.setLayout(layout_status)
        
        layout_home.addWidget(frame_title, 0, 0)
        layout_home.addWidget(frame_input, 1, 0)
        layout_home.addWidget(frame_status, 2, 0)

        self.home_tab.setLayout(layout_home)

    def init_test_bench_tab(self):
        # Set up the "Test Bench" tab layout and widgets
        layout2 = QVBoxLayout()
        self.commanded_temperature_tb = QLabel("Commanded Temperature: ")
        self.brake_state_tb = QLabel("Brake State: ")
        self.light_state_tb = QLabel("Light State: ")
        self.tunnel_label_tb = QLabel("In Tunnel: ")
        self.door_state_tb = QLabel("Door State: ")
        self.ki_value_tb = QLabel("KiValue: ")
        self.kp_value_tb = QLabel("KpValue: ")
        self.setpoint_velocity_tb = QLabel("Setpoint Velocity: ")
        self.commanded_power_tb = QLabel("Commanded Power: ")
        
        
        # Inputs and outputs with confirm buttons and labels
        layout2.addLayout(self.create_header("INPUTS:", 10))
        layout2.addLayout(self.create_line("Hour of Day: ", "Clock Time (integer 1-24)", self.set_hour))
        layout2.addLayout(self.create_line("Seconds of Day: ", "Clock Time (integer)", self.set_seconds))
    
        layout2.addLayout(self.create_header("AUTHORITY AND VELOCITY", 8))
        layout2.addLayout(self.create_line("Authority: ", "Meters (float)", self.set_commanded_authority))
        layout2.addLayout(self.create_line("Commanded Velocity: ", "m/s (0-19.44)", self.set_commanded_velocity))
        layout2.addLayout(self.create_line("Actual Velocity: ", "m/s (0-19.44)", self.set_actual_velocity))

        layout2.addLayout(self.create_header("FAILURE MODES", 8))
        layout2.addLayout(self.create_line("Brake Failure: ", "Bool (0/1)", self.set_brake_failure))
        layout2.addLayout(self.create_line("Engine Failure: ", "Bool (0/1)", self.set_engine_failure))
        layout2.addLayout(self.create_line("Signal Failure: ", "Bool (0/1)", self.set_signal_failure))

        layout2.addLayout(self.create_header("BEACON INFORMATION", 8))
        layout2.addLayout(self.create_line("Beacon Info: ", "ex. B1,2,Pioneer", self.set_beacon_information))
        layout2.addLayout(self.create_line("At Stop: ", "Bool (0/1)", self.set_at_stop))

        layout2.addLayout(self.create_header("OUTPUTS:", 10))
        layout2.addWidget(self.commanded_temperature_tb)
        layout2.addWidget(self.brake_state_tb)
        layout2.addWidget(self.light_state_tb)
        layout2.addWidget(self.tunnel_label_tb)
        layout2.addWidget(self.door_state_tb)
        layout2.addWidget(self.setpoint_velocity_tb)
        layout2.addWidget(self.ki_value_tb)
        layout2.addWidget(self.kp_value_tb)
        layout2.addWidget(self.commanded_power_tb)

        # Set layout to the test bench tab
        self.test_bench_tab.setLayout(layout2)

    def create_line(self, label_text, placeholder_text, confirm_function):
        # Helper to create a line with a label, input, and confirm button
        line_layout = QHBoxLayout()
        
        label = QLabel(label_text)
        textbox = QLineEdit()
        textbox.setPlaceholderText(placeholder_text)
        confirm_button = QPushButton("Confirm")

        label.setFixedSize = (250, 25)
        textbox.setFixedSize(100, 25)
        confirm_button.setFixedSize(100,25)

        confirm_button.clicked.connect(lambda: confirm_function(textbox.text()))
        #confirm_button.clicked.connect(lambda: self.write_to_serial())

        line_layout.addWidget(label)
        line_layout.addWidget(textbox)
        line_layout.addWidget(confirm_button)

        return line_layout 

    def create_header(self, input_title, size):
        # Helper to create a styled header label
        header_layout = QHBoxLayout()
        header = QLabel(input_title)
        font = header.font()
        font.setBold(True)
        font.setPointSize(size)
        header.setFont(font)
        header_layout.addWidget(header)

        return header_layout
    
    def open_serial_port(self):
        if self.com_input.text():
            self.serial_port = self.com_input.text()
        #else:
        #    self.serial_port = "COM3"
        if self.baud_input.text():
            self.baud_rate = self.baud_input.text()
        #else: 
        #    self.baud_rate = 9600

        try:
            # Attempt to open serial connection
            self.ser = serial.Serial(self.serial_port, int(self.baud_rate), timeout=1)
            if self.ser.is_open:
                self.connection_status.setText("Serial port opened successfully.")
                self.connection_status.setStyleSheet("color: green;")
                #self.status_label.setText("Arduino Status: Connected")
                print("Serial port opened successfully.")
        except (serial.SerialException, ValueError):
            self.connection_status.setText("ValueError")
            self.connection_status.setStyleSheet("color: red;")
            print("Error opening serial port:", ValueError)
            #self.status_label.setText("Arduino Status: Not Connected")


#SERIAL CONNECTION FUNCTIONS
    def read_serial(self):
        if self.ser and self.ser.in_waiting > 0:
            # Read a line from the serial connection
            line = self.ser.readline().decode().strip()

            #Split the comma-separated values
            #Line comes in the form of "commanded_temperature, brake_state, door_state, light_state, commanded_power"
            if line:
                values = line.split(',')
                if len(values) == 12:  # Ensure we have 12 values
                    self.compare_and_set(int(values[0]), self.commanded_temperature, self.set_commanded_temperature)
                     
                    self.e_brake_state = bool(values[1])

                    self.s_brake_state = bool(values[2])

                    self.ARD_outside_light_request = bool(values[3])

                    self.ARD_inside_light_request = bool(values[4])

                    self.left_door_request = bool(values[5])

                    self.right_door_request = bool(values[6])

                    self.compare_and_set(float(values[7]), self.setpoint_velocity, self.set_setpoint_velocity)

                    self.compare_and_set(float(values[8]), self.ki_value, self.set_ki_value)

                    self.compare_and_set(float(values[9]), self.kp_value, self.set_kp_value)

                    self.manual_mode = bool(values[10])

                    self.first_time_opening_doors = bool(values[11])
                    
                    self.actual_velocity = self.train_model_list[0].get_currentVelocity()
                    

                    #test bench items:
                    self.commanded_temperature_tb.setText(f"Commanded Temperature: {values[0]} Degrees F")
                    '''
                    self.brake_state_tb.setText(f"Brake State: {values[1]}")
                    self.door_state_tb.setText(f"Door State: {values[2]}")
                    self.light_state_tb.setText(f"Light State: {values[3]}")
                    self.tunnel_label_tb.setText(f"In Tunnel: {self.in_tunnel}")
                    self.ki_value_tb.setText(f"KiValue: {values[5]}")
                    self.kp_value_tb.setText(f"KpValue: {values[6]}")
                    self.setpoint_velocity_tb.setText(f"Setpoint Velocity: {values[4]}")
                    self.commanded_power_tb.setText(f"Commanded Power: {self.commanded_power}  Watts") 
                    '''  
                                
    def write_to_serial(self):
        #self.decode_beacon_info(self.beacon_info)

        #Continuously send backend variables to the serial port.
        #Create the command string using individual getter functions
        command = (         
            str(self.get_brake_state()) + "," +                                                 #0
            str(self.get_light_state()) + "," +                                              #1
            self.station_name + "," +                                                    #2
            str(self.get_brake_failure()) + "," +                                        #3
            str(self.get_engine_failure()) + "," +                                       #4
            str(self.get_signal_failure()) + "," +                                       #5
            str(self.meters_to_feet(self.get_current_authority())) + "," +               #6
            "{:.1f}".format(self.mps_to_mph(self.get_actual_velocity())) + "," +         #7
            "{:.1f}".format(self.mps_to_mph(self.get_commanded_velocity())) + "," +      #8
            str(self.get_door_state()) + "," +                                           #9
            "{:.3f}".format(self.get_commanded_power()) + "," +                          #10
            str(self.get_in_tunnel()) + "," +                                            #11
            str(self.brake_warning) + "\n"
        )
        self.ser.write(command.encode())

    def send_to_track_model(self, input):
        self.auth_diff_dict["auth_diff"] = input
        response = requests.post(URL + "/track-model/get-data/auth_difference", json=self.auth_diff_dict)
        print (f"UPDATED AUTHORITY: {input}")

    def compare_and_set(self, read_value, backend_value, set_function):
            if(read_value != backend_value):
                set_function(read_value)
            else:
                pass   

# TRAIN CONTROLLER LOGIC FUNCTIONS
    def controller_logic(self):
        if self.ser and self.ser.in_waiting > 0:
            if(not self.manual_mode):
                self.setpoint_velocity = self.commanded_velocity
                self.commanded_temperature = 68
            self.emergency_brake_handler
            self.service_brake_handler
            self.door_handler
            self.light_handler
            self.calculate_commanded_power
            self.update_current_authority
            self.read_serial
            self.write_to_serial

    def light_handler(self):
        if(self.manual_mode):
            #If the lights were set by the day of time in auto mode, turn them off and give control to driver
            if(self.lights_set_by_time):
                self.set_light_state(0)
                self.lights_set_by_time = False
            #Tunnel Handler
            if(self.in_tunnel):
                self.set_light_state(3)
                self.lights_set_by_tunnel = True
            else:
                if(self.lights_set_by_tunnel and not self.in_tunnel):
                    self.set_light_state(0)
                    self.lights_set_by_tunnel = False
                if(self.ARD_inside_light_request and not self.inside_light):
                    if(self.ARD_outside_light_request and not self.outside_light):
                        self.set_light_state(3)
                    self.set_light_state(2)
                elif(self.ARD_outside_light_request and not self.outside_light):
                    self.set_light_state(1)
        else:
            if((self.hour <= 7 or self.hour >= 20) and self.hour != 0):
                self.set_light_state(3)
                self.lights_set_by_time = True
            elif(self.in_tunnel):
                self.set_light_state(3)
                self.lights_set_by_tunnel = True
            else: 
                self.set_light_state(0)
                self.lights_set_by_time = False
                self.lights_set_by_tunnel = False

    def service_brake_handler(self):
        displacement = ((self.actual_velocity * self.actual_velocity) / 2.4)

        if(self.manual_mode):
            if(self.s_brake_state and self.brake_state != 1):
                self.set_brake_state(2)
            else:
                self.set_brake_state(0)
            if(not self.s_brake_state and self.brake_state != 1):
                if(self.current_authority <= displacement + self.feet_to_meters(20)):
                    self.brake_warning = True
                else:
                    self.brake_warning = False
            if(self.commanded_velocity == 0 and not self.s_brake_state and self.actual_velocity > self.commanded_velocity):
                self.brake_warning = True
            else:
                self.brake_warning = False
        else: #AUTO MODE
            if(self.brake_state != 1):
                if(self.current_authority <= displacement or self.actual_velocity > self.commanded_velocity):
                    self.set_brake_state(2)
                else:
                    self.set_brake_state(0)

    def emergency_brake_handler(self):
        if(self.e_brake_state == True): #from arduino (DRIVER)
            self.set_brake_state(1)
        elif(self.brake_state != 2):
            self.set_brake_state(0)

    def door_handler(self):
        #Runs automatically to open doors at the station
        if(self.actual_velocity == 0):
            if(self.at_stop and self.required_doors > 0 and self.first_time_opening_doors and self.current_authority <= 0):
                self.set_door_state(self.required_doors)
                self.right_door_request = self.right_door
                self.left_door_request = self.left_door
                self.first_time_opening_doors = False
            
            #left door timer
            if(self.reset_left_door_timer and (self.left_door_request or self.left_door)):
                self.temp_time_left = self.seconds
                self.reset_left_door_timer = False
                if(self.brake_state != 1):
                    self.set_brake_state(2)
            #right door timer
            if(self.reset_right_door_timer and (self.right_door_request or self.right_door)):
                self.temp_time_right = self.seconds
                self.reset_right_door_timer = False
                if(self.brake_state != 1):
                    self.set_brake_state(2)
                
            if(self.temp_time_left + 60 < self.seconds):
                self.reset_left_door_timer = True
                self.left_door = False 
                self.left_door_request = False   

            if(self.temp_time_right + 60 < self.seconds):
                self.reset_right_door_timer = True
                self.right_door = False 
                self.right_door_request = False  


            if(self.left_door and self.right_door):
                self.set_door_state(3)
            elif(self.left_door and not self.right_door):
                self.set_door_state(2)
            elif(not self.left_door and self.right_door):
                self.set_door_state(1)
            else:
                self.set_door_state(0)
                if(self.brake_state != 1 and not self.s_brake_state):
                    self.set_brake_state(0)
        else:
            self.first_time_opening_doors = True

    def decode_beacon_info(self, encoded_beacon_info):
        if encoded_beacon_info:
            values = encoded_beacon_info.split(',')
            #this decodes the 3 segments of information
            if len(values) == 3:
                #checks if station beacon
                if values[0][0] == "B" or "b":
                    self.current_beacon_identifier = values[0]

                    if (self.current_beacon_identifier != self.previous_beacon_identifier):
                        self.at_stop = not(self.at_stop)

                        if(self.previous_beacon_identifier == "T2"):
                            self.in_tunnel = not(self.in_tunnel)
                    
                    self.previous_beacon_dentifier = self.current_beacon_identifier
                    self.required_doors = values[1]

                    #set pa announcement string
                    if self.current_authority < 180:
                        self.station_name = values[2]
                        self.set_pa_announcement(self.station_name, self.at_stop)
                
            elif len(values) == 1:
                #check if tunnel beacon
                if values[0][0] == "T" or values[0][0] == "t":
                    self.current_beacon_identifier = values[0]
                    if (self.current_beacon_identifier != self.previous_beacon_identifier):
                        self.in_tunnel = not(self.in_tunnel)    #flip in_tunnel bool
                        self.previous_beacon_dentifier = self.current_beacon_identifier

                    #self.required_doors = values[1]

                    #set pa announcement string
                    if self.current_authority < 180:
                        self.station_name = values[2]
                        self.set_pa_announcement(self.station_name, self.at_stop)

    def update_current_authority(self):
        if(self.train_instantion == True):
            self.set_current_authority(self.commanded_authority + self.current_authority)
            if(self.current_authority > 0):
                self.train_instantion = False
        if(self.current_authority <= 0 and self.actual_velocity == 0 and self.first_time_opening_doors == False):
            self.set_current_authority(self.commanded_authority + self.current_authority) 
        else:
            self.current_authority -= self.actual_velocity*self.T
            self.difference_in_authority += self.actual_velocity*self.T

        if self.counter_authority >= 40:
            self.send_to_track_model(self.difference_in_authority)
            self.difference_in_authority = 0
            self.counter_authority = 1
        else:
            self.counter_authority += 1

    def calculate_commanded_power(self):
        v_command = self.setpoint_velocity
        v_error = v_command - self.actual_velocity
        self.ek_previous = self.ek_current
        self.ek_current = v_error

        if self.commanded_power < 120000:
            self.uk_current = self.uk_previous + (self.T/2)*(self.ek_current + self.ek_previous)
        elif self.commanded_power >= 120000:
            self.uk_current = self.uk_previous

        self.commanded_power = (self.kp_value * self.ek_current) + (self.ki_value * self.uk_current)

        if self.brake_state != 0 :
            self.commanded_power = 0.0
        elif self.commanded_power < 0.0:
            self.commanded_power = 0.0
        elif self.door_state > 0:
            self.commanded_power = 0.0
        elif self.manual_mode and (self.mph_to_mps(self.setpoint_velocity) < self.actual_velocity):
            self.commanded_power = 0.0

        self.set_commanded_power(self.commanded_power)


# UNIT CONVERSIONS
    def kmph_to_mph(self, input):
        return (float(input)/1.609344)

    def kmph_to_mps(self, input):
        return (float(input)/3.6)

    def mps_to_mph(self, input):
        return (float(input)*2.237)

    def mph_to_mps(self, input):
        return (float(input)/2.237)

    def meters_to_feet(self, input):
        return (float(input)*3.28084)

    def feet_to_meters(self, input):
        return (float(input)/3.28084)
















#Set Functions:
#========================================================
    def set_connection_status(self, input):
        self.connection_status = input

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
        response = requests.post(URL + "/train-model/receive-temperature", json=self.temperature_dict)

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

        response = requests.post(URL + "/train-model/receive-brakes", json=self.brakes_dict)

    def set_door_state(self, input):
        self.door_state = input

        if(self.door_state == 0):
            self.set_left_door_state(False)
            self.set_right_door_state(False)
        elif(self.door_state == 1):
            self.set_left_door_state(False)
            self.set_right_door_state(True)
        elif(self.door_state == 2):
            self.set_left_door_state(True)
            self.set_right_door_state(False)
        elif(self.door_state == 3):
            self.set_left_door_state(True)
            self.set_right_door_state(True)

        response = requests.post(URL + "/train-model/receive-doors", json=self.doors_dict)

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

        response = requests.post(URL + "/train-model/receive-lights", json=self.lights_dict)

    def set_commanded_power(self, input):
        self.commanded_power = float(input)
        #self.commanded_power_dict["commanded_power"] = self.commanded_power
        #response = requests.post(URL + "/train-model/receive-commanded-power", json=self.commanded_power_dict)
        self.train_model_list[0].set_commanded_power(self.commanded_power)
        
    def set_required_doors(self, input):
        self.required_doors = input
    
    def set_hour(self, input):
        self.hour = input
        #self.write_to_serial()
    
    def set_seconds(self, input):
        self.seconds = input
        #self.write_to_serial()

    def set_brake_failure(self, input):
        self.brake_failure = int(input)
        #self.write_to_serial()
    
    def set_engine_failure(self, input):
        self.engine_failure = int(input)
        #self.write_to_serial()

    def set_signal_failure(self, input):
        self.signal_failure = int(input)
        #self.write_to_serial()

    def set_commanded_authority(self, input): 
        self.commanded_authority = input
        #self.write_to_serial()

    def set_current_authority(self, input):
        self.current_authority = input
        #self.write_to_serial()

    def set_actual_velocity(self, input):
        self.actual_velocity = input 
        #self.write_to_serial()

    def set_commanded_velocity(self, input):
        #self.commanded_velocity = self.mps_to_mph(input)
        self.commanded_velocity = input
        #self.write_to_serial()

    def set_beacon_information(self, input):
        self.beacon_information = input
        self.decode_beacon_info(self.beacon_information)
        #self.write_to_serial()

    def set_beacon_identifier(self, input):
        self.beacon_identifier = input  

    def set_pa_announcement(self, input, entering):
        if entering:
            self.pa_announcement = "Arriving at:" + input
        else: 
            self.pa_announcement = "Deaparting from " + input
        
        self.pa_announcement_dict["pa_announcement"] = self.pa_announcement
        response = requests.post(URL + "/train-model/receive-announcement", json=self.pa_announcement_dict)

    def set_at_stop(self, input):
        self.at_stop = input
        #self.write_to_serial()

    def set_T(self, input):
        self.T = input

    def set_setpoint_velocity(self, input):
        setpt = self.mph_to_mps(input)
        if self.commanded_velocity < setpt:
            self.setpoint_velocity = self.commanded_velocity
        elif input < 0:
            self.setpoint_velocity = 0
        else:
            self.setpoint_velocity = setpt

    def set_ki_value(self, input):
        self.ki_value = input

    def set_kp_value(self, input):
        self.kp_value = input

    def set_manual_mode(self, input):
        self.manual_mode = input

    def set_sim_speed(self, input):
        self.sim_speed = input

        self.set_T(0.09 * self.sim_speed)


#Get Functions:
#========================================================
    def get_in_tunnel(self):
        return self.in_tunnel

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

    def get_commanded_power(self):
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

    def get_commanded_authority(self):
        self.commanded_authority = float(input)
        self.update_current_authority()

    def get_current_authority(self):
        return self.current_authority

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
    
    def get_sim_speed(self):
        return self.sim_speed
        
    def get_T(self):
        return self.T

    def get_setpoint_velocity(self):
        return self.setpoint_velocity
    
    def get_manual_mode(self):
        return self.manual_mode

    def get_ki_value(self):
        return self.ki_value
    
    def get_kp_value(self):
        return self.kp_value
