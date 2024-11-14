import time
import sys

from Train_Controller_SW.Train_Controller_SW_Class import Train_Controller
#from Train_Controller_SW_Class import Train_Controller


from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QStackedLayout,
    QFrame,
    QTabWidget,
    QStackedWidget,
)

#list of trains
# train_list =[] 




# self.add_train()
# self.add_train()
# self.add_train()
# self.train_list[0].authority = 200
# self.train_list[1].authority = 250
# self.train_list[2].authority = 100

# self.train_list[0].actual_velocity = 10
# self.train_list[0].commanded_velocity = 18
# self.train_list[0].setpoint_velocity = 14

# self.train_list[1].actual_velocity = 11
# self.train_list[1].commanded_velocity = 7
# self.train_list[1].setpoint_velocity = 7

# self.train_list[2].actual_velocity = 8
# self.train_list[2].commanded_velocity = 12
# self.train_list[2].setpoint_velocity = 12


class Train_Controller_SW_UI(QMainWindow):

    def __init__(self):
        super(Train_Controller_SW_UI, self).__init__()


        self.next_train_id = 0
        self.train_list =[]

        self.add_train()
        self.add_train()
        self.add_train()
        self.train_list[0].authority = 0
        self.train_list[1].authority = 250
        self.train_list[2].authority = 100

        self.train_list[0].actual_velocity = 10
        self.train_list[0].commanded_velocity = 18
        self.train_list[0].setpoint_velocity = 14

        self.train_list[1].actual_velocity = 11
        self.train_list[1].commanded_velocity = 7
        self.train_list[1].setpoint_velocity = 7

        self.train_list[2].actual_velocity = 8
        self.train_list[2].commanded_velocity = 12
        self.train_list[2].setpoint_velocity = 12

        #set a fixed window size
        self.setFixedSize(800, 550)

        self.setWindowTitle("Train Controller Software - Micah Smith")
        
        

        #############################################
        #OVerall design setup
        #############################################
        
        self.stacked_widget = QStackedWidget()

        #setting up control widget and layout
        self.control_widget = QWidget()
        self.control_layout = QGridLayout(self.control_widget)

        #test bench widget and layout
        self.test_bench_widget = QWidget()
        self.test_bench_layout = QGridLayout(self.test_bench_widget)

        #two tabs: main control and test bench
        self.stacked_widget.addWidget(self.control_widget)
        self.stacked_widget.addWidget(self.test_bench_widget)

        #need 2 buttons to switch between control and test bench
        self.test_bench_button = QPushButton("Test Bench")
        self.test_bench_button.clicked.connect(self.to_test_bench)


        self.control_button = QPushButton("Main Controls")
        self.control_button.clicked.connect(self.to_control)

        #set the layout to be the tabs
        self.setCentralWidget(self.stacked_widget)

        #this is a font which we will use for most of the UI
        custom_font = self.create_custom_font()
        important_font = self.important_custom_font()
        

        #this font will be used for inputs
        input_font = self.font()  # Get the default font
        input_font.setPointSize(11)
        input_font.setFamily("Manrope")  #Manrope
        input_font.setBold(False)  #Bold

        #############################################
        #Train Selection Tab
        #############################################

        #create dropdown menu with 3 trains in it already
        self.train_selection = QComboBox(self)
        self.train_selection.addItems(["Train 0", "Train 1", "Train 2"])

        # Sends the current index (position) of the selected item.
        self.train_selection.currentIndexChanged.connect( self.index_changed )
        self.train_selection.setFont(custom_font)

        #get value of current index of train
        self.current_train = self.train_selection.currentIndex()

        self.train_selection.setEditable(True)

        #############################################
        #Driver and Engineer Sections
        #############################################
        driver_widget = QLabel("Driver")
        driver_widget.setFont(custom_font)


        engineer_layout = QVBoxLayout()
        engineer_frame = QFrame()
        engineer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        engineer_frame.setFrameShadow(QFrame.Shadow.Raised)
        engineer_frame.setLineWidth(3)
        engineer_frame.setLayout(engineer_layout)
        

        #set Engineer Label to be at center top of engineer_frame
        engineer_label = QLabel("Engineer", engineer_frame)
        engineer_label.setFont(custom_font)
        engineer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #
        # 
        #  kp frame
        kp_ki_layout = QGridLayout()
        kp_ki_frame = QFrame()
        kp_ki_frame.setLayout(kp_ki_layout)
        
        #setting up Kp widgets
        kp_label = QLabel("Kp:")
        kp_label.setFont(custom_font)

        self.kp_button = QPushButton("Confirm", kp_ki_frame)
        self.kp_button.clicked.connect(self.confirm_kp)
        self.kp_button.setFont(custom_font)
        self.kp_button.setStyleSheet(
            """
    QPushButton 
    {
        background-color: green;
        color: white;
        border: 3px solid #4CAF50;
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:hover 
    {
        background-color: #45A049;  /* button is lighter when hovering over it */
    }
    QPushButton:pressed 
    {
        background-color: #2E7D32;  /* button becomes darker when pressed */
    }
    """)
        
        #this widget will represent where you can enter Kp
        self.input_kp = QLineEdit(kp_ki_frame)
        self.input_kp.setFont(input_font)
        self.input_kp.setPlaceholderText(f"{self.train_list[self.current_train].k_p}")

        ki_label = QLabel("Ki:")
        ki_label.setFont(custom_font)

        self.ki_button = QPushButton("Confirm", kp_ki_frame)
        self.ki_button.clicked.connect(self.confirm_ki)
        self.ki_button.setFont(custom_font)
        self.ki_button.setStyleSheet(
            """
    QPushButton 
    {
        background-color: green;
        color: white;
        border: 3px solid #4CAF50;
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:hover 
    {
        background-color: #45A049;  /* button is lighter when hovering over it */
    }
    QPushButton:pressed 
    {
        background-color: #2E7D32;  /* button becomes darker when pressed */
    }
    """)

        #this widget will represent where you can enter in Ki
        self.input_ki = QLineEdit(kp_ki_frame)
        self.input_ki.setFont(input_font)
        self.input_ki.setPlaceholderText(f"{self.train_list[self.current_train].k_i}")

        #adding kp and kp widgets to frame
        kp_ki_layout.addWidget(kp_label, 0, 0)
        kp_ki_layout.addWidget(self.input_kp, 0, 1)
        kp_ki_layout.addWidget(self.kp_button, 0, 2)
        kp_ki_layout.addWidget(ki_label, 1, 0)
        kp_ki_layout.addWidget(self.input_ki, 1, 1)
        kp_ki_layout.addWidget(self.ki_button, 1, 2)

        #adding kp/ki frame and engineer label
        engineer_layout.addWidget(engineer_label)
        engineer_layout.addWidget(kp_ki_frame)

        #############################################
        #Authority Tab
        #############################################

        #create frame
        authority_frame = QFrame()
        authority_frame.setFrameShape(QFrame.Shape.StyledPanel)
        authority_frame.setFrameShadow(QFrame.Shadow.Raised)
        authority_frame.setLineWidth(3)

        self.authority_layout = QVBoxLayout()
        authority_frame.setLayout(self.authority_layout)


        #we create the authority text and put inside the frame
        self.authority_widget = QLabel(f'<span style="color: #C598FF;"> &nbsp; Authority: </span> <span style="color: white;">{self.meters_to_feet(self.train_list[0].get_authority())} ft</span>')
        self.authority_widget.setFont(important_font)

        #add widget to layout
        self.authority_layout.addWidget(self.authority_widget)


        #############################################
        #Velocity Tab
        #############################################

        #create frame for velocities
        velocities_layout = QVBoxLayout()
        velocities_frame = QFrame()
        velocities_frame.setFrameShape(QFrame.Shape.StyledPanel)
        velocities_frame.setFrameShadow(QFrame.Shadow.Raised)
        velocities_frame.setLineWidth(3)

        #now we create all QLabels for the 3 velocity values and set their fonts
        #self.actual_velocity_widget = QLabel(f"  Actual Velocity: {self.mps_to_mph(self.train_list[0].actual_velocity)} MPH", velocities_frame)
        
        self.actual_velocity_widget = QLabel(f'<span style="color: #C598FF;"> &nbsp; Actual Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[0].get_actual_velocity())} MPH</span>', velocities_frame)
       
        self.actual_velocity_widget.setFont(important_font)

        self.commanded_velocity_widget = QLabel(f'<span style="color: #C598FF;"> &nbsp; Commanded Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[0].get_commanded_velocity())} MPH</span>', velocities_frame)
        self.commanded_velocity_widget.setFont(important_font)

        self.setpoint_velocity_widget = QLabel(f'<span style="color: #C598FF;"> &nbsp; Setpoint Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[0].get_setpoint_velocity())} MPH</span>', velocities_frame)
        self.setpoint_velocity_widget.setFont(important_font)

        #create layout and frame for inputting new setpoint velocity
        setpoint_velocity_frame = QFrame()
        setpoint_velocity_layout = QHBoxLayout(setpoint_velocity_frame)

        #this widget will represent where you can enter in setpoint speed
        self.input_setpoint_velocity = QLineEdit(velocities_frame)
        self.input_setpoint_velocity.setPlaceholderText("Setpoint Velocity (MPH)")

        self.input_setpoint_velocity.setFont(input_font)
        
        
        #confirm button
        self.setpoint_velocity_button = QPushButton("Confirm", velocities_frame)
        self.setpoint_velocity_button.clicked.connect(self.confirm_setpoint_velocity)
        self.setpoint_velocity_button.setFont(custom_font)
        self.setpoint_velocity_button.setStyleSheet(
            """
    QPushButton 
    {
        background-color: green;
        color: white;
        border: 3px solid #4CAF50;
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:hover 
    {
        background-color: #45A049;  /* button is lighter when hovering over it */
    }
    QPushButton:pressed 
    {
        background-color: #2E7D32;  /* button becomes darker when pressed */
    }
    """)

        #add to horizontal layout
        setpoint_velocity_layout.addWidget(self.input_setpoint_velocity)
        setpoint_velocity_layout.addWidget(self.setpoint_velocity_button)

        #add the widgets to the velocities_layout
        velocities_layout.addWidget(self.actual_velocity_widget)
        velocities_layout.addWidget(self.commanded_velocity_widget)
        velocities_layout.addWidget(self.setpoint_velocity_widget)
        velocities_layout.addWidget(setpoint_velocity_frame)

        #set the frame to have the velocties layout
        velocities_frame.setLayout(velocities_layout)

        #############################################
        #Doors
        #############################################

        #set up door frame and layout
        doors_layout = QGridLayout()
        doors_frame = QFrame()
        doors_frame.setFrameShape(QFrame.Shape.StyledPanel)
        doors_frame.setFrameShadow(QFrame.Shadow.Raised)
        doors_frame.setLineWidth(3)

        #set frame to have doors_layout
        doors_frame.setLayout(doors_layout)

        #left door
        l_door_label = QLabel("Left Doors:", doors_frame)
        l_door_label.setFont(custom_font)

        #left door button
        self.l_door_button = QPushButton("Closed", doors_frame)
        self.l_door_button.setFont(custom_font)
        self.l_door_button.clicked.connect(self.open_l_door)

        #create a timer which will be connected to doors so they open for 60 seconds
        self.l_door_timer = QTimer(self)
        self.l_door_timer.setSingleShot(True)
        self.l_door_timer.timeout.connect(self.close_l_door)


        #right door
        r_door_label = QLabel("Right Doors:", doors_frame)
        r_door_label.setFont(custom_font)

        #right door button
        self.r_door_button = QPushButton("Closed", doors_frame)
        self.r_door_button.setFont(custom_font)
        self.r_door_button.clicked.connect(self.open_r_door)

        #create a timer which will be connected to doors so they open for 60 seconds
        self.r_door_timer = QTimer(self)
        self.r_door_timer.setSingleShot(True)
        self.r_door_timer.timeout.connect(self.close_r_door)




        #add widgets to layout
        doors_layout.addWidget(l_door_label, 0, 0)
        doors_layout.addWidget(self.l_door_button, 0, 1)
        doors_layout.addWidget(r_door_label, 1, 0)
        doors_layout.addWidget(self.r_door_button, 1, 1)


        #############################################
        #Lights
        #############################################

        #set up light frame and layout
        light_layout = QGridLayout()
        light_frame = QFrame()
        light_frame.setFrameShape(QFrame.Shape.StyledPanel)
        light_frame.setFrameShadow(QFrame.Shadow.Raised)
        light_frame.setLineWidth(3)

        #set frame to have light_layout
        light_frame.setLayout(light_layout)

        #create widgets for inside light 
        i_light_label = QLabel("Inside Lights:", light_frame)
        i_light_label.setFont(custom_font)
        
        self.i_light_button = QPushButton("💡 OFF")
        self.i_light_button.setStyleSheet("background-color: gray;")
        self.i_light_button.setFont(custom_font)
        self.i_light_button.clicked.connect(self.i_light_pressed)



        #create widgets for headlights
        o_light_label = QLabel("Headlights:", light_frame)
        o_light_label.setFont(custom_font)

        self.o_light_button = QPushButton("💡 OFF")
        self.o_light_button.setStyleSheet("background-color: gray;")
        self.o_light_button.setFont(custom_font)
        self.o_light_button.clicked.connect(self.o_light_pressed)

        #add the widgets to the layout
        light_layout.addWidget(i_light_label, 0, 0)
        light_layout.addWidget(o_light_label, 1, 0)
        light_layout.addWidget(self.i_light_button, 0, 1)
        light_layout.addWidget(self.o_light_button, 1, 1)


        #############################################
        #Set Temperature
        #############################################
        
        #create frame for temp tab
        temperature_layout = QVBoxLayout()
        temperature_frame = QFrame()
        temperature_frame.setFrameShape(QFrame.Shape.StyledPanel)
        temperature_frame.setFrameShadow(QFrame.Shadow.Raised)
        temperature_frame.setLineWidth(3)
        
        #label for temperature
        set_temperature_widget = QLabel("Set Temperature",temperature_frame)
        set_temperature_widget.setFont(custom_font)

        #QSpinBox for arrow keys to set temperature
        self.temperature_control = QSpinBox()
        self.temperature_control.setMinimum(65)
        self.temperature_control.setMaximum(75)
        self.temperature_control.setSuffix("°F")
        self.temperature_control.setFont(custom_font)

        self.temperature_control.setValue(self.train_list[self.train_selection.currentIndex()].get_temperature())

        self.temperature_control.valueChanged.connect(self.temperature_changed)  #calls function whenever temperature is changed


        #add temperaute label and arrow key
        temperature_layout.addWidget(set_temperature_widget)
        temperature_layout.addWidget(self.temperature_control)

        #set layout to be in frame
        temperature_frame.setLayout(temperature_layout)



        #############################################
        #Errors
        #############################################

        #setup frame andd layout for errors tab
        error_layout = QGridLayout()
        error_frame = QFrame()
        error_frame.setFrameShape(QFrame.Shape.StyledPanel)
        error_frame.setFrameShadow(QFrame.Shadow.Raised)
        error_frame.setLineWidth(3)
        error_frame.setLayout(error_layout)

        #make labels
        engine_failure_label = QLabel("Engine Failure:", error_frame)
        engine_failure_label.setFont(custom_font)

        brake_failure_label = QLabel("Brake Failure:", error_frame)
        brake_failure_label.setFont(custom_font)

        signal_failure_label = QLabel("Signal Failure:", error_frame)
        signal_failure_label.setFont(custom_font)



        #now we create the error lights
        self.engine_light = QLabel(error_frame)
        self.engine_light.setFixedSize(20,20)

        self.brake_light = QLabel(error_frame)
        self.brake_light.setFixedSize(20,20)


        self.signal_light = QLabel(error_frame)
        self.signal_light.setFixedSize(20,20)



        error_layout.addWidget(engine_failure_label, 0, 0)
        error_layout.addWidget(self.engine_light, 0, 1)
        error_layout.addWidget(brake_failure_label, 1, 0)
        error_layout.addWidget(self.brake_light, 1, 1)
        error_layout.addWidget(signal_failure_label, 2, 0)
        error_layout.addWidget(self.signal_light, 2, 1)
        
        

        


        #############################################
        #Manual Mode
        #############################################

        #automatically in manual mode
        self.manual_widget = QCheckBox("Manual Mode")
        self.manual_widget.setChecked(False)
        self.manual_widget.setFont(custom_font)
        
        #function is called when checkbox changes
        self.manual_widget.stateChanged.connect(self.manual_widget_changed)

        #############################################
        #Service Brake and Emergency Brake
        #############################################
        
        #frame and layout for brakes
        brake_layout = QHBoxLayout()
        brake_frame = QFrame()
        brake_frame.setLayout(brake_layout)

        #font for brakes
        brake_font = self.font()  # Get the default font
        brake_font.setPointSize(16)
        brake_font.setFamily("Manrope")  #Manrope
        brake_font.setBold(True)  #Bold

        self.s_brake_button = QPushButton("BRAKE", brake_frame)
        self.s_brake_button.setFont(brake_font)

        self.e_brake_button = QPushButton("E-BRAKE", brake_frame)
        self.e_brake_button.setFont(brake_font)
        self.e_brake_button.setCheckable(True)
        

        self.s_brake_button.setStyleSheet(
            """
    QPushButton 
    {
        background-color: #D39927;
        color: white;
        border: 3px solid #B3791F;
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:hover 
    {
        background-color: #E0A84D;  /* button is lighter when hovering over it */
    }
    QPushButton:pressed 
    {
        background-color: #A56B1A;  /* button becomes darker when pressed */
    }
    QPushButton:checked
            {
                background-color: #A56B1A;  /* button becomes darker when pressed */
            }
    """)

        self.e_brake_button.setStyleSheet(
            """
    QPushButton 
    {
        background-color: red;
        color: white;
        border: 3px solid #FF1A1A;
        border-radius: 10px;
        padding: 5px;
    }
    QPushButton:hover 
    {
        background-color: #FF6666;  /* button is lighter when hovering over it */
    }
    QPushButton:pressed 
    {
        background-color: #CC0000;  /* button becomes darker when pressed */
    }
    QPushButton:checked
            {
                background-color: #CC0000;  /* button becomes darker when pressed */
            }
    """)
        
        #service brake is pressed
        self.s_brake_button.pressed.connect(self.s_brake_pressed)
        self.s_brake_button.released.connect(self.s_brake_released)




        #emergency brake is clicked
        self.e_brake_button.clicked.connect(self.e_brake_clicked)

        #add buttons to frame
        brake_layout.addWidget(self.s_brake_button)
        brake_layout.addWidget(self.e_brake_button)

        #############################################
        #Addding the frames to the Controls UI
        #############################################
        
        #divider between first two columns
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.VLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)
        self.divider.setLineWidth(3)
        self.control_layout.addWidget(self.divider, 0, 1, 4, 1)

        self.control_layout.addWidget(engineer_frame, 3, 1+1)
        self.control_layout.addWidget(authority_frame, 0, 1+1)
        self.control_layout.addWidget(self.train_selection, 1, 0)
        self.control_layout.addWidget(velocities_frame, 1, 1+1)
        self.control_layout.addWidget(temperature_frame, 0, 2+1)
        self.control_layout.addWidget(light_frame, 1, 2+1)
        self.control_layout.addWidget(doors_frame, 2, 2+1)
        self.control_layout.addWidget(self.manual_widget, 0, 0)
        self.control_layout.addWidget(error_frame, 3, 2+1)
        self.control_layout.addWidget(brake_frame, 2, 1+1)
        self.control_layout.addWidget(self.control_button, 2, 0)
        self.control_layout.addWidget(self.test_bench_button, 3, 0)

        #all widgets should be disabled since default is auto mode
        self.manual_mode()


        #############################################
        #All Test Bench Widgets
        #############################################

        test_bench_label_font = self.font()  # Get the default font
        test_bench_label_font.setPointSize(16)
        test_bench_label_font.setFamily("Manrope")  #Manrope
        test_bench_label_font.setBold(True)  #Bold

        #input label widget
        input_label = QLabel("INPUTS")
        input_label.setFont(test_bench_label_font)

        self.test_bench_layout.addWidget(input_label, 0, 2)


        #condense code since all these input fields involve putting text in
        self.input_authority = self.test_bench_input("Authority:", self.confirm_authority, 1)
        self.input_actual_velocity = self.test_bench_input("Actual Velocity:", self.confirm_actual_velocity, 2)
        self.input_commanded_velocity = self.test_bench_input("Commanded Velocity:", self.confirm_commanded_velocity, 3)
        self.input_beacon_info = self.test_bench_input("Beacon Info:", self.confirm_beacon_info, 4)

        #set units
        self.input_authority.setPlaceholderText("ft")
        self.input_commanded_velocity.setPlaceholderText("MPH")
        self.input_actual_velocity.setPlaceholderText("MPH")
        self.input_beacon_info.setPlaceholderText("String")


        #Code for failure mode inputs
        self.input_engine_failure = self.test_bench_failure("Engine Failure", self.engine_failure_changes, 5)
        self.input_brake_failure = self.test_bench_failure("Brake Failure", self.brake_failure_changes, 6)
        self.input_signal_failure = self.test_bench_failure("Signal Failure", self.signal_failure_changes, 7)

        #output label widget
        output_label = QLabel("OUTPUTS")
        output_label.setFont(test_bench_label_font)

        self.test_bench_layout.addWidget(output_label, 0, 3)

        #outputs to be displayed 
        
        self.commanded_power_output = QLabel(f'<span style="color: #C598FF;"> &nbsp; Commanded Power: </span> <span style="color: white;">{self.train_list[self.current_train].get_commanded_power():.2f} Watts</span>')
        self.pa_announcement_output = QLabel(f"PA Announcement: {self.train_list[self.current_train].get_pa_announcement()}")

        self.commanded_power_output.setFont(important_font)

        #add widget to authority layout
        self.authority_layout.addWidget(self.commanded_power_output)

        #add widgets
        self.test_bench_layout.addWidget(self.pa_announcement_output, 2, 3)



        
        #fill in the failures lights correctly
        self.check_errors()

        # Create a QTimer for computing power
        self.power_timer = QTimer(self)
        self.power_timer.timeout.connect(self.calculate_power)  # Connect the timer to your function
        self.power_timer.start(50)  # 50 milliseconds interval



    #############################################
    #Functions for setting Failure inputs
    #############################################

    def test_bench_failure(self, input_label, failure_changes, row):
        #setup label for field
        check_box = QCheckBox(input_label)
        check_box.setChecked(False)

        #connect to function when state changes
        check_box.stateChanged.connect(failure_changes)

        #add temp frame to test_bench_layout
        self.test_bench_layout.addWidget(check_box, row, 2)         

        #return edit box
        return check_box
    
    #failure functions
    def engine_failure_changes(self, state):
        #checks if box is checked
        if state == 2:
            self.train_list[self.current_train].set_failure_engine(True)
        else:
            self.train_list[self.current_train].set_failure_engine(False)

    def brake_failure_changes(self, state):
        #checks if box is checked
        if state == 2:
            self.train_list[self.current_train].set_failure_brake(True)
        else:
            self.train_list[self.current_train].set_failure_brake(False)

    def signal_failure_changes(self, state):
        #checks if box is checked
        if state == 2:
            self.train_list[self.current_train].set_failure_signal(True)
        else:
            self.train_list[self.current_train].set_failure_signal(False)


    #############################################
    #Functions for setting Numerical inputs
    ############################################

    def test_bench_input(self, input_label, confirm_func, row):
        
        #setup layout and frame for input
        temp_layout = QHBoxLayout()
        temp_frame = QFrame()
        temp_frame.setLayout(temp_layout)

        #setup label for field
        label = QLabel(input_label)
        input_field = QLineEdit()


        #confirm button set up to connect to function
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(confirm_func)

        #combine 3 elements into layout
        temp_layout.addWidget(label)
        temp_layout.addWidget(input_field)
        temp_layout.addWidget(confirm_button)

        #add temp frame to test_bench_layout
        self.test_bench_layout.addWidget(temp_frame, row, 2)         

        #return edit box
        return input_field

    #called when authority input is confirmed
    def confirm_authority(self):
        # Get the text from the input field and update the label
        input_value = self.input_authority.text()

        #update label  
        self.input_authority.setPlaceholderText(input_value)
        self.input_authority.setText("")

        #set authority in train list
        self.train_list[self.current_train].set_authority(self.feet_to_meters(float(input_value)))

        print(f"authority: {self.train_list[self.current_train].get_authority()} meters")

    #called when actual velocity input is confirmed
    def confirm_actual_velocity(self):
        # Get the text from the input field and update the label
        input_value = self.input_actual_velocity.text()

        #update label  
        self.input_actual_velocity.setPlaceholderText(input_value)
        self.input_actual_velocity.setText("")

        #set actual velocity in train list as metric
        self.train_list[self.current_train].set_actual_velocity(self.mph_to_mps(float(input_value)))

        print(f"actual velocity: {self.train_list[self.current_train].get_actual_velocity()} m/s")

    #called when commanded velocity input is confirmed
    def confirm_commanded_velocity(self):
        # Get the text from the input field and update the label
        input_value = self.input_commanded_velocity.text()

        #update label  
        self.input_commanded_velocity.setPlaceholderText(input_value)
        self.input_commanded_velocity.setText("")

        #set commanded in train list
        self.train_list[self.current_train].set_commanded_velocity(self.mph_to_mps(float(input_value)))

        print(f"commanded velocity: {self.train_list[self.current_train].get_commanded_velocity()} m/s")

    #called when beacon info input is confirmed
    def confirm_beacon_info(self):
        # Get the text from the input field and update the label
        input_value = str(self.input_beacon_info.text())

        #update label
        self.input_beacon_info.setPlaceholderText(input_value)
        self.input_beacon_info.setText("")

        #set beacon info in train list
        self.train_list[self.current_train].set_beacon_info(input_value)

        #test
        print(self.train_list[self.current_train].get_pa_announcement())
        print("fries")

        #update display on test bench
        self.update_outputs()





    #This function will update all other information in UI to match the train which was selected
    def index_changed(self, i): # i is an int which represent the index of the train
        print(f"Train {i} has been selected")

        self.current_train = i

        #clear out all inputs
        self.input_setpoint_velocity.clear()
        self.input_authority.clear()
        self.input_commanded_velocity.clear()
        self.input_actual_velocity.clear()
        self.input_beacon_info.clear()

        self.input_authority.setPlaceholderText("ft")
        self.input_commanded_velocity.setPlaceholderText("MPH")
        self.input_actual_velocity.setPlaceholderText("MPH")
        self.input_beacon_info.setPlaceholderText("String")



        #update every widget in the UI

        self.authority_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Authority: </span> <span style="color: white;">{self.meters_to_feet(self.train_list[i].get_authority())} ft</span>')

        self.actual_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Actual Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[i].get_actual_velocity())} MPH</span>')
        
        self.commanded_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Commanded Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[i].get_commanded_velocity())} MPH</span>')
        
        self.setpoint_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Setpoint Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[i].get_setpoint_velocity())} MPH</span>')

        self.temperature_control.setValue(self.train_list[i].get_temperature())
        
        #check inside light
        if self.train_list[i].get_i_light() == True:
            #light must turn on
            self.i_light_button.setText("💡 ON")
            self.i_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.i_light_button.setText("💡 OFF")
            self.i_light_button.setStyleSheet("background-color: gray;")

        #check headlight
        if self.train_list[i].get_o_light() == True:
            #light must turn on
            self.o_light_button.setText("💡 ON")
            self.o_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.o_light_button.setText("💡 OFF")
            self.o_light_button.setStyleSheet("background-color: gray;")


        # Update door status for the train
        if self.train_list[i].get_l_door() == True:
            self.l_door_button.setText("Opened")
            self.l_door_button.setEnabled(False)
        else:
            self.l_door_button.setText("Closed")
            self.l_door_button.setEnabled(True)

        if self.train_list[i].get_r_door() == True:
            self.r_door_button.setText("Opened")
            self.r_door_button.setEnabled(False)
        else:
            self.r_door_button.setText("Closed")
            self.r_door_button.setEnabled(True)

        #set kp and Ki values
        self.input_kp.setPlaceholderText(f"{self.train_list[i].k_p}")
        self.input_ki.setPlaceholderText(f"{self.train_list[i].k_i}")

        if self.train_list[self.current_train].get_e_brake() == True:      #sets e_brake_staus to opposite status
            self.e_brake_button.setChecked(True)
        else:
            self.e_brake_button.setChecked(False)
        
        #checks if there are any current failures
        if self.train_list[self.current_train].check_any_failures() and self.train_list[self.current_train].get_e_brake() == True:
            self.e_brake_button.setEnabled(False)
        else:
            self.e_brake_button.setEnabled(True)
        

        #check manual mode
        self.manual_mode()


        #check for errors
        self.check_errors()

        #update outputs in test bench
        self.update_outputs()
        



    
    #this function will setup the custom font that we will use for all widgets
    def create_custom_font(self):
        
        #we will set up the font here
        custom_font = self.font()  # Get the default font
        custom_font.setPointSize(13)
        custom_font.setFamily("Manrope")  #Manrope
        custom_font.setBold(True)  #Bold
        return custom_font

    def important_custom_font(self):
        
        #we will set up the font here
        custom_font = self.font()  # Get the default font
        custom_font.setPointSize(15)
        custom_font.setFamily("Manrope")  #Manrope
        custom_font.setBold(True)  #Bold
        return custom_font
    

    #function is called when setpoint velocity is put in
    def confirm_setpoint_velocity(self):
        # Get the text from the input field and update the label
        input_value = self.mph_to_mps(float(self.input_setpoint_velocity.text()))

        #checks if input value is less allowed by commanded velocity
        if input_value <= self.train_list[self.current_train].get_commanded_velocity() and input_value >= 0 :
            self.train_list[self.current_train].set_setpoint_velocity(input_value)
        #if value is greater than commanded, then we set it automatically to commanded velocity
        elif input_value > self.train_list[self.current_train].get_commanded_velocity() :
            self.train_list[self.current_train].set_setpoint_velocity(self.train_list[self.current_train].get_commanded_velocity())

        #update label
        self.setpoint_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Setpoint Velocity: </span> <span style="color: white;">{int(self.mps_to_mph(self.train_list[self.current_train].get_setpoint_velocity()))} MPH</span>')


    #this function will be called whenever the temperature is changed
    def temperature_changed(self, temperature):

        #update train temperature
        self.train_list[self.train_selection.currentIndex()].set_temperature(temperature)

        print(temperature)

    #this function will be called anytime inside lights button is pressed 
    def i_light_pressed(self):
        #checks if light is currently on or off
        if self.train_list[self.current_train].get_i_light() == False:
            #light must turn on
            self.train_list[self.current_train].set_i_light(True)
            self.i_light_button.setText("💡 ON")
            self.i_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.train_list[self.current_train].set_i_light(False)
            self.i_light_button.setText("💡 OFF")
            self.i_light_button.setStyleSheet("background-color: gray;")

    #this function will be called anytime inside headlights button is pressed 
    def o_light_pressed(self):
        #checks if light is currently on or off
        if self.train_list[self.current_train].get_o_light() == False:
            #light must turn on
            self.train_list[self.current_train].set_o_light(True)
            self.o_light_button.setText("💡 ON")
            self.o_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.train_list[self.current_train].set_o_light(False)
            self.o_light_button.setText("💡 OFF")
            self.o_light_button.setStyleSheet("background-color: gray;")

    #this function handles when the l_door_button is pressed
    def open_l_door(self):
        #updates signal to tell train model to open door
        self.train_list[self.current_train].set_l_door(True)
        self.train_list[self.current_train].set_doors_can_open(False)

        #disables button
        self.l_door_button.setEnabled(False)

        #change button text
        self.l_door_button.setText("Opened")

        #start 60s timer
        self.l_door_timer.start(4000)

        print(f"The current train is {self.current_train}")

    #activates door button again
    def close_l_door(self):
        #door is now closed
        self.train_list[self.current_train].set_l_door(False)

        #change text back
        self.l_door_button.setText("Closed")

        #activates door button again if in manual mode
        if self.train_list[self.current_train].get_manual_mode():
            self.l_door_button.setEnabled(True)


        print(f"The current train is {self.current_train}")
    

    #this function handles when the l_door_button is pressed
    def open_r_door(self):
        #updates signal to tell train model to open door
        self.train_list[self.current_train].set_r_door(True)
        self.train_list[self.current_train].set_doors_can_open(False)

        #disables button
        self.r_door_button.setEnabled(False)

        #change button text
        self.r_door_button.setText("Opened")

        #start 60s timer
        self.r_door_timer.start(4000)

    #activates door button again
    def close_r_door(self):
        #door is now closed
        self.train_list[self.current_train].set_r_door(False)

        #change text back
        self.r_door_button.setText("Closed")

        #activates door button again if in manual mode
        if self.train_list[self.current_train].get_manual_mode():
            self.r_door_button.setEnabled(True)

    #handles when manual mode is turned on or off
    def manual_widget_changed(self, state):
        #checks if box is checked
        if state == 2:
            self.train_list[self.current_train].set_manual_mode(True)
        else:
            self.train_list[self.current_train].set_manual_mode(False)

        #call manual_mode function to enable/disable widgets
        self.manual_mode()

    def manual_mode(self):

        if self.train_list[self.current_train].get_manual_mode() == True:
            #enable all widgets
            self.manual_widget.setChecked(True)
            self.input_setpoint_velocity.setEnabled(True)
            self.setpoint_velocity_button.setEnabled(True)
            self.l_door_button.setEnabled(True)
            self.r_door_button.setEnabled(True)
            self.o_light_button.setEnabled(True)
            self.i_light_button.setEnabled(True)
            self.temperature_control.setEnabled(True)
            self.s_brake_button.setEnabled(True)

            #auto brake turns off
            self.s_brake_released()
            self.s_brake_button.setCheckable(False)
            self.s_brake_button.setChecked(False)
        else:
            #disable all widgets
            self.manual_widget.setChecked(False)
            self.input_setpoint_velocity.setEnabled(False)
            self.setpoint_velocity_button.setEnabled(False)
            self.l_door_button.setEnabled(False)
            self.r_door_button.setEnabled(False)
            self.o_light_button.setEnabled(False)
            self.i_light_button.setEnabled(False)
            self.temperature_control.setEnabled(False)
            self.s_brake_button.setEnabled(False)
            #self.s_brake_button.setCheckable(True)
            #self.s_brake_button.setChecked(True)
            

    def check_errors(self):
        if self.train_list[self.current_train].get_failure_engine() == True:
            self.engine_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
            #update test bench
            self.input_engine_failure.setChecked(True)
        else:
            self.engine_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)

            #update test bench
            self.input_engine_failure.setChecked(False)
            
        if self.train_list[self.current_train].get_failure_brake() == True:
            self.brake_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
            #update test bench
            self.input_brake_failure.setChecked(True)

        else:
            self.brake_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
            #update test bench
            self.input_brake_failure.setChecked(False)
            
        if self.train_list[self.current_train].get_failure_signal() == True:
            self.signal_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
            #update test bench
            self.input_signal_failure.setChecked(True)

        else:
            self.signal_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
            #update test bench
            self.input_signal_failure.setChecked(False)
            
    #handles when service brake is pressed
    def s_brake_pressed(self):
        self.train_list[self.current_train].set_s_brake(True)  #sets bool to true when pressed
        #print("Service Brake Pressed")

     #handles when service brake is released
    def s_brake_released(self):
        self.train_list[self.current_train].set_s_brake(False)  #sets bool back to false when released
        #print("Service Brake Released")


    #hands when emergency brake is clicked
    def e_brake_clicked(self):
        if self.train_list[self.current_train].get_e_brake() == False:      #sets e_brake_staus to opposite status
            self.train_list[self.current_train].set_e_brake(True)
            self.e_brake_button.setChecked(True)
        else:
            self.train_list[self.current_train].set_e_brake(False)
            self.e_brake_button.setChecked(False)
        
        #checks if there are any current failures
        if self.train_list[self.current_train].check_any_failures():
            self.e_brake_button.setEnabled(False)

        #set set-speed to 0 which in turn turns off power
        #self.train_list[self.current_train].setpoint_velocity = 0
        #self.setpoint_velocity_widget.setText(f"  Setpoint Velocity: {self.mps_to_mph(self.train_list[self.current_train].setpoint_velocity)} MPH")

        #call the brake function to slow down train

    def confirm_kp(self):
        # Get the text from the input field and update the label
        input_value = float(self.input_kp.text())

        #update label  
        self.input_kp.setPlaceholderText(str(input_value))
        self.input_kp.setText("")

        #set kp in train list
        self.train_list[self.current_train].set_k_p(input_value)

    def confirm_ki(self):
        # Get the text from the input field and update the label
        input_value = float(self.input_ki.text())

        #update label  
        self.input_ki.setPlaceholderText(str(input_value))
        self.input_ki.setText("")

        #set kp in train list
        self.train_list[self.current_train].set_k_i(input_value)

    #switches to test bench screen
    def to_test_bench(self):

        #update screen
        self.stacked_widget.setCurrentIndex(1)

        #add overlayed widgets
        self.test_bench_layout.addWidget(self.commanded_power_output, 1, 3)
        self.test_bench_layout.addWidget(self.control_button, 2, 0)
        self.test_bench_layout.addWidget(self.test_bench_button, 3, 0)
        self.test_bench_layout.addWidget(self.train_selection, 1, 0)
        self.test_bench_layout.addWidget(self.manual_widget, 0, 0)
        self.test_bench_layout.addWidget(self.divider, 0, 1, 8, 1)

        #adjust commanded power text
        self.commanded_power_output.setFont(QFont())

        

    #switches to control screen
    def to_control(self):
        
        #update information
        self.index_changed(self.current_train)

        #update screen
        self.stacked_widget.setCurrentIndex(0)

        #add overlayed widgets
        self.authority_layout.addWidget(self.commanded_power_output)
        self.control_layout.addWidget(self.control_button, 2, 0)
        self.control_layout.addWidget(self.test_bench_button, 3, 0)
        self.control_layout.addWidget(self.train_selection, 1, 0)
        self.control_layout.addWidget(self.manual_widget, 0, 0)
        self.control_layout.addWidget(self.divider, 0, 1, 4, 1)

        #adjust commanded power text
        self.commanded_power_output.setFont(self.important_custom_font())


    #updates all outputs
    def update_outputs(self):
        #update test bench outputs

        self.commanded_power_output.setText(f'<span style="color: #C598FF;"> &nbsp; Commanded Power: </span> <span style="color: white;">{self.train_list[self.current_train].get_commanded_power():.2f} Watts</span>')

        #self.commanded_power_output.setText(f"Commanded Power: {self.train_list[self.current_train].get_commanded_power:.2f} Watts")
        self.pa_announcement_output.setText(f"PA Announcement: {self.train_list[self.current_train].get_pa_announcement()}")


        #self.train_list[self.current_train].beacon_info = "Lebron"


    #convert meters per second to miles per hour
    def mps_to_mph(self, metric_speed):
        return int(metric_speed * 2.237)
    
    #converts miles per hour to meters per second
    def mph_to_mps(self, imperial_speed):
        return imperial_speed / 2.237
    
    #convert meters to feet
    def meters_to_feet(self, metric):
        return int(metric*3.28084)

    #convert meters to feet
    def feet_to_meters(self, imperial):
        return imperial/3.28084
    
    #function that calculates power and does all other timed function
    def calculate_power(self):
        
        #if received authority is negative, then that means we are supposed to receive new authority
        if self.train_list[self.current_train].get_received_authority() > 0 and self.train_list[self.current_train].get_can_get_authority():
            self.train_list[self.current_train].set_authority_to_received()
            self.train_list[self.current_train].set_can_get_authority(False)                                                    #COMMENT THIS OUT TO TEST WITHOUT THIS FUNCTION

        #updates UI info
        self.authority_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Authority: </span> <span style="color: white;">{self.meters_to_feet(self.train_list[self.current_train].get_authority())} ft</span>')

        self.actual_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Actual Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[self.current_train].get_actual_velocity())} MPH</span>')
        
        self.commanded_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Commanded Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[self.current_train].get_commanded_velocity())} MPH</span>')
        
        self.check_errors()

        #checks if train is in manual mode
        #If in auto, sets setpoint velocity to commanded and automatically brakes if setpoint velocity is below actual velocity
        if self.train_list[self.current_train].get_manual_mode() == False:
            self.train_list[self.current_train].set_setpoint_velocity(self.train_list[self.current_train].get_commanded_velocity())            #set setpoint equal to commanded

            #first we ehck if train has to brake to stop at a station
            if self.train_list[self.current_train].stop_at_station() == True:
                self.s_brake_pressed()
                self.s_brake_button.setCheckable(True)
                self.s_brake_button.setChecked(True)
            elif self.train_list[self.current_train].get_setpoint_velocity() < self.train_list[self.current_train].get_actual_velocity() and self.train_list[self.current_train].get_e_brake() == False:
                self.s_brake_pressed()
                self.s_brake_button.setCheckable(True)
                self.s_brake_button.setChecked(True)
            else:
                self.s_brake_released()
                self.s_brake_button.setChecked(False)
                self.s_brake_button.setCheckable(False)


        #if e_brake is pressed, checks if it can be unpressed
        if self.train_list[self.current_train].get_e_brake() == True:
            if self.train_list[self.current_train].check_any_failures() == False:
                self.e_brake_button.setEnabled(True)
                #print(self.train_list[self.current_train].get_e_brake())

        #make sure setpoint can not exceed commanded
        self.train_list[self.current_train].SetSetPointVelocity()

        self.setpoint_velocity_widget.setText(f'<span style="color: #C598FF;"> &nbsp; Setpoint Velocity: </span> <span style="color: white;">{self.mps_to_mph(self.train_list[self.current_train].get_setpoint_velocity())} MPH</span>') #update setpoint 
           
        #calculate power
        self.train_list[self.current_train].calculate_commanded_power()

        #update authority
        self.train_list[self.current_train].update_authority()

        #update power in test bench
        self.commanded_power_output.setText(f'<span style="color: #C598FF;"> &nbsp; Commanded Power: </span> <span style="color: white;">{self.train_list[self.current_train].get_commanded_power():.2f} Watts</span>')


        #print(str(self.train_list[self.current_train].get_authority()))
        #check if doors have to open if train has stopped, auhority is 0, and doors haven't opened

        if self.train_list[self.current_train].get_authority() <= 0.0 and self.train_list[self.current_train].get_actual_velocity() == 0.0 and self.train_list[self.current_train].get_doors_can_open():
            
            #checks which doors to open
            doors = self.train_list[self.current_train].get_doors_to_open()

            print(doors)
            #opens correct doors based off decoded beacon info
            if doors == "3":
                self.open_l_door()
                self.open_r_door()
            elif doors == "2":
                self.open_l_door()
            elif doors == "1":
                self.open_r_door()
    

    def add_train(self):
        new_train = Train_Controller(self.next_train_id)
        self.next_train_id += 1
        self.train_list.append(new_train)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Train_Controller_SW_UI()
    window.show()

    sys.exit(app.exec())



# app = QApplication(sys.argv)
# w = Train_Controller_SW_UI()
# w.show()
# app.exec()

