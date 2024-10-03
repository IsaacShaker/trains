import time
import sys

from Train_Controller_SW import Train_Controller

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
    QFrame
)

#list of trains
train_list =[] 

def add_train():
    new_train = Train_Controller()
    train_list.append(new_train)


add_train()
add_train()
add_train()
train_list[0].authority = 1000
train_list[1].authority = 600
train_list[2].authority = 50

train_list[0].actual_velocity = 10
train_list[0].commanded_velocity = 30
train_list[0].setpoint_velocity = 20

train_list[1].actual_velocity = 41
train_list[1].commanded_velocity = 61
train_list[1].setpoint_velocity = 51

train_list[2].actual_velocity = 12
train_list[2].commanded_velocity = 32
train_list[2].setpoint_velocity = 22






class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        #set a fixed window size
        self.setFixedSize(700, 500)

        self.setWindowTitle("Train Controller Software - Micah Smith")


        #setting up layout to be a grid
        main_widget = QWidget(self)
        layout = QGridLayout(main_widget)

        #this is a font which we will use for the whole UI
        custom_font = self.create_custom_font()

        #############################################
        #Driver and Engineer Labels
        #############################################
        driver_widget = QLabel("Driver",self)
        driver_widget.setFont(custom_font)

        engineer_widget = QLabel("Engineer", self)
        engineer_widget.setFont(custom_font)


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

        #############################################
        #Authority Tab
        #############################################

        #create frame
        authority_frame = QFrame()
        authority_frame.setFrameShape(QFrame.Shape.StyledPanel)
        authority_frame.setFrameShadow(QFrame.Shadow.Raised)
        authority_frame.setLineWidth(3)
        #authority_frame.setStyleSheet("background-color: #232323;")


        #we create the authority text and put inside the frame
        self.authority_widget = QLabel(f"  Authority: {train_list[0].authority} ft", authority_frame)
        self.authority_widget.setFont(custom_font)


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
        self.actual_velocity_widget = QLabel(f"  Actual Velocity: {train_list[0].actual_velocity} MPH", velocities_frame)
        self.actual_velocity_widget.setFont(custom_font)

        self.commanded_velocity_widget = QLabel(f"  Commanded Velocity: {train_list[0].commanded_velocity} MPH", velocities_frame)
        self.commanded_velocity_widget.setFont(custom_font)

        self.setpoint_velocity_widget = QLabel(f"  Setpoint Velocity: {train_list[0].setpoint_velocity} MPH", velocities_frame)
        self.setpoint_velocity_widget.setFont(custom_font)

        #create layout and frame for inputting new setpoint velocity
        setpoint_velocity_frame = QFrame()
        setpoint_velocity_layout = QHBoxLayout(setpoint_velocity_frame)

        #this widget will represent where you can enter in setpoint speed
        self.input_setpoint_velocity = QLineEdit(velocities_frame)
        self.input_setpoint_velocity.setPlaceholderText("Setpoint Velocity (MPH)")
        self.input_setpoint_velocity.setFont(custom_font)
        
        #confirm button
        self.confirm_setpoint_velocity = QPushButton("Confirm", velocities_frame)
        self.confirm_setpoint_velocity.clicked.connect(self.on_confirm)
        self.confirm_setpoint_velocity.setFont(custom_font)
        self.confirm_setpoint_velocity.setStyleSheet(
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
        setpoint_velocity_layout.addWidget(self.confirm_setpoint_velocity)

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
        self.l_door_button = QPushButton("Open", doors_frame)
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
        self.r_door_button = QPushButton("Open", doors_frame)
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

        self.temperature_control.setValue(train_list[self.train_selection.currentIndex()].temperature)

        self.temperature_control.valueChanged.connect(self.value_changed)  #calls function whenever temperature is changed


        #add temperaute label and arrow key
        temperature_layout.addWidget(set_temperature_widget)
        temperature_layout.addWidget(self.temperature_control)

        #set layout to be in frame
        temperature_frame.setLayout(temperature_layout)



        #############################################
        #Errors
        #############################################




        #############################################
        #Manual Mode
        #############################################

        #automatically in manual mode
        self.manual_widget = QCheckBox("Manual Mode")
        self.manual_widget.setChecked(False)
        self.manual_widget.setFont(custom_font)
        
        #function is called when checkbox changes
        self.manual_widget.stateChanged.connect(self.manual_widget_changes)





        #############################################
        #Addding the frames to the UI
        #############################################
        layout.addWidget(driver_widget, 1, 0)
        layout.addWidget(engineer_widget, 5, 0)
        layout.addWidget(authority_frame, 2, 0)
        layout.addWidget(self.train_selection, 0, 0)
        layout.addWidget(velocities_frame, 3, 0)
        layout.addWidget(temperature_frame, 3, 1)
        layout.addWidget(light_frame, 2, 1)
        layout.addWidget(doors_frame, 1, 1)
        layout.addWidget(self.manual_widget, 0, 1)


        #all widgets should be disabled since default is auto mode
        self.input_setpoint_velocity.setEnabled(False)
        self.confirm_setpoint_velocity.setEnabled(False)
        self.l_door_button.setEnabled(False)
        self.r_door_button.setEnabled(False)
        self.o_light_button.setEnabled(False)
        self.i_light_button.setEnabled(False)
        self.temperature_control.setEnabled(False)

        #set the layout
        self.setCentralWidget(main_widget)


    #This function will update all other information in UI to match the train which was selected
    def index_changed(self, i): # i is an int which represent the index of the train
        print(f"Train {i} has been selected")

        self.current_train = i

        #update every widget in the UI
        self.authority_widget.setText(f"  Authority: {train_list[i].authority} ft")
        self.actual_velocity_widget.setText(f"  Actual Velocity: {train_list[i].actual_velocity} MPH")
        self.commanded_velocity_widget.setText(f"  Commanded Velocity: {train_list[i].commanded_velocity} MPH")
        self.setpoint_velocity_widget.setText(f"  Setpoint Velocity: {train_list[i].setpoint_velocity} MPH")
        self.temperature_control.setValue(train_list[i].temperature)
        
        #check inside light
        if train_list[i].i_light == True:
            #light must turn on
            self.i_light_button.setText("💡 ON")
            self.i_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.i_light_button.setText("💡 OFF")
            self.i_light_button.setStyleSheet("background-color: gray;")

        #check headlight
        if train_list[i].o_light == True:
            #light must turn on
            self.o_light_button.setText("💡 ON")
            self.o_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            self.o_light_button.setText("💡 OFF")
            self.o_light_button.setStyleSheet("background-color: gray;")


        # Update door status for the train
        if train_list[i].l_door == True:
            self.l_door_button.setText("Operating")
            self.l_door_button.setEnabled(False)
        else:
            self.l_door_button.setText("Open")
            self.l_door_button.setEnabled(True)

        if train_list[i].r_door == True:
            self.r_door_button.setText("Operating")
            self.r_door_button.setEnabled(False)
        else:
            self.r_door_button.setText("Open")
            self.r_door_button.setEnabled(True)

        #check manual mode
        self.manual_mode()


    
    #this function will setup the custom font that we will use for all widgets
    def create_custom_font(self):
        
        #we will set up the font here
        custom_font = self.font()  # Get the default font
        custom_font.setPointSize(14)
        custom_font.setFamily("Manrope")  #Manrope
        custom_font.setBold(True)  #Bold
        return custom_font
    

    def on_confirm(self):
        # Get the text from the input field and update the label
        input_value = int(self.input_setpoint_velocity.text())

        #checks if input value is less allowed by commanded velocity
        if input_value <= train_list[self.current_train].commanded_velocity and input_value >= 0 :
            train_list[self.current_train].setpoint_velocity = input_value
        #if value is greater than commanded, then we set it automatically to commanded velocity
        elif input_value > train_list[self.current_train].commanded_velocity :
            train_list[self.current_train].setpoint_velocity = train_list[self.current_train].commanded_velocity

        #update label  
        self.setpoint_velocity_widget.setText(f"  Setpoint Velocity: {train_list[self.current_train].setpoint_velocity} MPH")


    #this function will be called whenever the temperature is changed
    def value_changed(self, temperature):

        #update train temperature
        train_list[self.train_selection.currentIndex()].temperature = temperature

        print(temperature)

    #this function will be called anytime inside lights button is pressed 
    def i_light_pressed(self):
        #checks if light is currently on or off
        if train_list[self.current_train].i_light == False:
            #light must turn on
            train_list[self.current_train].i_light = True
            self.i_light_button.setText("💡 ON")
            self.i_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            train_list[self.current_train].i_light = False
            self.i_light_button.setText("💡 OFF")
            self.i_light_button.setStyleSheet("background-color: gray;")

    #this function will be called anytime inside headlights button is pressed 
    def o_light_pressed(self):
        #checks if light is currently on or off
        if train_list[self.current_train].o_light == False:
            #light must turn on
            train_list[self.current_train].o_light = True
            self.o_light_button.setText("💡 ON")
            self.o_light_button.setStyleSheet("background-color: yellow; color:black")
        else:
            #light must turn off
            train_list[self.current_train].o_light = False
            self.o_light_button.setText("💡 OFF")
            self.o_light_button.setStyleSheet("background-color: gray;")

    #this function handles when the l_door_button is pressed
    def open_l_door(self):
        #updates signal to tell train model to open door
        train_list[self.current_train].l_door = True

        #disables button
        self.l_door_button.setEnabled(False)

        #change button text
        self.l_door_button.setText("Operating")

        #start 60s timer
        self.l_door_timer.start(4000)

        print(f"The current train is {self.current_train}")

    #activates door button again
    def close_l_door(self):
        #door is now closed
        train_list[self.current_train].l_door = False

        #change text back
        self.l_door_button.setText("Open")

        #activates door button again
        self.l_door_button.setEnabled(True)

        print(f"The current train is {self.current_train}")
    

    #this function handles when the l_door_button is pressed
    def open_r_door(self):
        #updates signal to tell train model to open door
        train_list[self.current_train].r_door = True

        #disables button
        self.r_door_button.setEnabled(False)

        #change button text
        self.r_door_button.setText("Operating")

        #start 60s timer
        self.r_door_timer.start(4000)

    #activates door button again
    def close_r_door(self):
        #door is now closed
        train_list[self.current_train].r_door = False

        #change text back
        self.r_door_button.setText("Open")

        #activates door button again
        self.r_door_button.setEnabled(True)

    #handles when manual mode is turned on or off
    def manual_widget_changes(self, state):
        #checks if box is checked
        if state == 2:
            train_list[self.current_train].manual_mode = True
        else:
            train_list[self.current_train].manual_mode = False

        #call manual_mode function to enable/disable widgets
        self.manual_mode()

    def manual_mode(self):
        if train_list[self.current_train].manual_mode == True:
            #enable all widgets
            self.manual_widget.setChecked(True)
            self.input_setpoint_velocity.setEnabled(True)
            self.confirm_setpoint_velocity.setEnabled(True)
            self.l_door_button.setEnabled(True)
            self.r_door_button.setEnabled(True)
            self.o_light_button.setEnabled(True)
            self.i_light_button.setEnabled(True)
            self.temperature_control.setEnabled(True)
        else:
            #disable all widgets
            self.manual_widget.setChecked(False)
            self.input_setpoint_velocity.setEnabled(False)
            self.confirm_setpoint_velocity.setEnabled(False)
            self.l_door_button.setEnabled(False)
            self.r_door_button.setEnabled(False)
            self.o_light_button.setEnabled(False)
            self.i_light_button.setEnabled(False)
            self.temperature_control.setEnabled(False)
            



    
        





app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()

