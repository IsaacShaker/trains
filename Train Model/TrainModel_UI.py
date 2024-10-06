import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt


class UserModePage(QWidget):
    def __init__(self):
        super().__init__()

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the top section (Image)
        top_layout = QHBoxLayout()

        # Display an image using a relative path
        image_label = QLabel()
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'kennywood_ad.jpg')
        pixmap = QPixmap(image_path).scaled(700, 150, Qt.AspectRatioMode.KeepAspectRatio)  # Adjust size as needed
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(image_label)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)

        # Announcement Label
        announcement_label = QLabel("Announcement:")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))  # Set font size for the announcement label
        announcement_text = QLabel("Stay clear of doors")
        announcement_text.setFont(QFont('Arial', 20, QFont.Weight.Bold))  # Set larger font for the announcement text
        announcement_text.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the announcement text
        main_layout.addWidget(announcement_label)
        main_layout.addWidget(announcement_text)

        # Create a horizontal layout for left and right sections for group boxes
        horizontal_layout = QHBoxLayout()

        # Create left layout for Speed, Dimensions, and Train Status
        left_layout = QVBoxLayout()

        # Create right layout for Lights/Doors and Failure Modes
        right_layout = QVBoxLayout()

        # Emergency Brake Button
        emergency_brake_button = QPushButton("Emergency Brake")
        emergency_brake_button.setStyleSheet("background-color: red; color: white;")
        emergency_brake_button.setFixedHeight(50)
        left_layout.addWidget(emergency_brake_button)

        # Create and style Speed Information Group Box
        speed_group_box = QGroupBox("Speed Information")
        speed_layout = QVBoxLayout()

        # Velocity
        velocity_layout = QHBoxLayout()
        velocity_layout.addWidget(QLabel("Velocity:"))
        velocity_label = QLabel("60 mph")  # Change from button to QLabel
        velocity_layout.addWidget(velocity_label)
        speed_layout.addLayout(velocity_layout)

        # Acceleration
        acceleration_layout = QHBoxLayout()
        acceleration_layout.addWidget(QLabel("Acceleration:"))
        acceleration_label = QLabel("2 feet/s²")  # Change from button to QLabel
        acceleration_layout.addWidget(acceleration_label)
        speed_layout.addLayout(acceleration_layout)

        speed_group_box.setLayout(speed_layout)

        # Create and style Train Dimensions Group Box
        train_dimensions_group_box = QGroupBox("Train Dimensions")
        train_dimensions_layout = QVBoxLayout()

        # Length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Length:"))
        length_label = QLabel("105.6 ft")  # Change from button to QLabel
        length_layout.addWidget(length_label)
        train_dimensions_layout.addLayout(length_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        width_label = QLabel("8.6 ft")  # Change from button to QLabel
        width_layout.addWidget(width_label)
        train_dimensions_layout.addLayout(width_layout)

        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        height_label = QLabel("11.2 ft")  # Change from button to QLabel
        height_layout.addWidget(height_label)
        train_dimensions_layout.addLayout(height_layout)

        # Mass
        mass_layout = QHBoxLayout()
        mass_layout.addWidget(QLabel("Mass:"))
        mass_label = QLabel("90,000 lbs")  # Change from button to QLabel
        mass_layout.addWidget(mass_label)
        train_dimensions_layout.addLayout(mass_layout)

        # Number of Cars
        num_cars_layout = QHBoxLayout()
        num_cars_layout.addWidget(QLabel("Number of Cars:"))
        num_cars_label = QLabel("1")  # Change from button to QLabel
        num_cars_layout.addWidget(num_cars_label)
        train_dimensions_layout.addLayout(num_cars_layout)

        train_dimensions_group_box.setLayout(train_dimensions_layout)

        # Create and style Train Status Group Box
        train_status_group_box = QGroupBox("Train Status")
        train_status_layout = QVBoxLayout()

        # Passenger Count
        passenger_count_layout = QHBoxLayout()
        passenger_count_layout.addWidget(QLabel("Passenger Count:"))
        passenger_count_label = QLabel("50")  # Change from button to QLabel
        passenger_count_layout.addWidget(passenger_count_label)
        train_status_layout.addLayout(passenger_count_layout)

        # Crew Count
        crew_count_layout = QHBoxLayout()
        crew_count_layout.addWidget(QLabel("Crew Count:"))
        crew_count_label = QLabel("2")  # Change from button to QLabel
        crew_count_layout.addWidget(crew_count_label)
        train_status_layout.addLayout(crew_count_layout)

        # Temperature
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(QLabel("Temperature:"))
        temperature_label = QLabel("68 °F")  # Change from button to QLabel
        temperature_layout.addWidget(temperature_label)
        train_status_layout.addLayout(temperature_layout)

        train_status_group_box.setLayout(train_status_layout)

        # Add group boxes to left layout
        left_layout.addWidget(speed_group_box)
        left_layout.addWidget(train_dimensions_group_box)
        left_layout.addWidget(train_status_group_box)

        # Lights and Doors - Group box for door states
        doors_group_box = QGroupBox("Doors")
        doors_layout = QVBoxLayout()

        # Right Door
        right_door_layout = QHBoxLayout()
        right_door_layout.addWidget(QLabel("Right Door:"))
        self.right_door_label = QLabel("Closed")  # Change from button to QLabel
        self.right_door_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the door state
        self.right_door_label.setStyleSheet("background-color: green; padding: 5px;")  # Default color
        right_door_layout.addWidget(self.right_door_label)
        doors_layout.addLayout(right_door_layout)

        # Left Door
        left_door_layout = QHBoxLayout()
        left_door_layout.addWidget(QLabel("Left Door:"))
        self.left_door_label = QLabel("Closed")  # Change from button to QLabel
        self.left_door_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the door state
        self.left_door_label.setStyleSheet("background-color: green; padding: 5px;")  # Default color
        left_door_layout.addWidget(self.left_door_label)
        doors_layout.addLayout(left_door_layout)

        doors_group_box.setLayout(doors_layout)
        right_layout.addWidget(doors_group_box)

        # Lights - Labels showing the state in a box
        lights_group_box = QGroupBox("Lights")
        lights_layout = QVBoxLayout()

        # Headlights
        headlights_layout = QHBoxLayout()
        headlights_layout.addWidget(QLabel("Headlights:"))
        self.headlights_label = QLabel("Off")  # Change from button to QLabel
        self.headlights_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the headlight state
        self.headlights_label.setStyleSheet("background-color: gray; padding: 5px;")  # Default color
        headlights_layout.addWidget(self.headlights_label)
        lights_layout.addLayout(headlights_layout)

        # Inside Lights
        inside_lights_layout = QHBoxLayout()
        inside_lights_layout.addWidget(QLabel("Inside Lights:"))
        self.inside_lights_label = QLabel("Off")  # Change from button to QLabel
        self.inside_lights_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the inside light state
        self.inside_lights_label.setStyleSheet("background-color: gray; padding: 5px;")  # Default color
        inside_lights_layout.addWidget(self.inside_lights_label)
        lights_layout.addLayout(inside_lights_layout)

        lights_group_box.setLayout(lights_layout)
        right_layout.addWidget(lights_group_box)

        # Failure Modes Section
        failure_modes_group_box = QGroupBox("Failure Modes")
        failure_modes_layout = QVBoxLayout()

        # Failure mode buttons in red
        engine_button = QPushButton("Engine")
        brake_button = QPushButton("Brake")
        signal_pickup_button = QPushButton("Signal Pickup")

        # Set buttons to red
        engine_button.setStyleSheet("background-color: red; color: white;")
        brake_button.setStyleSheet("background-color: red; color: white;")
        signal_pickup_button.setStyleSheet("background-color: red; color: white;")

        failure_modes_layout.addWidget(engine_button)
        failure_modes_layout.addWidget(brake_button)
        failure_modes_layout.addWidget(signal_pickup_button)
        failure_modes_group_box.setLayout(failure_modes_layout)
        right_layout.addWidget(failure_modes_group_box)

        # Add both layouts to the horizontal layout
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(right_layout)

        # Add horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Set the main layout to the main widget
        self.setLayout(main_layout)

    def update_headlights_state(self, headlights_on):
        self.headlights_label.setText("On" if headlights_on else "Off")
        self.headlights_label.setStyleSheet("background-color: yellow;" if headlights_on else "background-color: gray;")

    def update_inside_lights_state(self, inside_lights_on):
        self.inside_lights_label.setText("On" if inside_lights_on else "Off")
        self.inside_lights_label.setStyleSheet("background-color: yellow;" if inside_lights_on else "background-color: gray;")

    def update_door_states(self, right_door_open, left_door_open):
        self.right_door_label.setText("Open" if right_door_open else "Closed")
        self.right_door_label.setStyleSheet("background-color: red;" if right_door_open else "background-color: green;")
        
        self.left_door_label.setText("Open" if left_door_open else "Closed")
        self.left_door_label.setStyleSheet("background-color: red;" if left_door_open else "background-color: green;")

class SelectTrainPage(QWidget):
    def __init__(self):
        super().__init__()

        # List of available trains
        available_trains = ["Train 0", "Train 1", "Train 2", "Train 3"]

        # Set a larger font for the title
        title_font = QFont('Arial', 20, QFont.Weight.Bold)
        label_font = QFont('Arial', 14)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the layout

        # Title Section
        self.selected_train_display = QLabel("Selected Train: ")
        self.selected_train_display.setFont(title_font)
        self.selected_train_display.setStyleSheet("color: white;")

        self.selected_train_number = QLabel("Train 1")  # Default selected train number
        self.selected_train_number.setFont(title_font)
        self.selected_train_number.setStyleSheet("color: white;")

        selected_train_layout = QHBoxLayout()
        selected_train_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_train_layout.addWidget(self.selected_train_display)
        selected_train_layout.addWidget(self.selected_train_number)
        layout.addLayout(selected_train_layout)

        # Instructions
        select_train_txt = QLabel("Select a train to view and press confirm")
        select_train_txt.setFont(label_font)
        # For any QLabel where you see a box behind the text

        select_train_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(select_train_txt)

        # Create dropdown (combo box) for train selection
        self.train_dropdown = QComboBox()
        self.train_dropdown.addItems(available_trains)
        self.train_dropdown.setFont(label_font)
        layout.addWidget(self.train_dropdown)

        # Button to confirm selection with improved styling
        select_train_button = QPushButton("Confirm Train Selection")
        select_train_button.setFont(label_font)
        select_train_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 15px 20px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        select_train_button.clicked.connect(self.select_train)
        layout.addWidget(select_train_button)

        layout.addStretch()
        self.setLayout(layout)

    def select_train(self):
        selected_train = self.train_dropdown.currentText()  # Get selected train
        self.selected_train_number.setText(selected_train)  # Update label to show selection
        # Add more logic to handle the selected train (e.g., pass it to another system)

class TestBenchPage(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the Test Bench
        layout = QVBoxLayout()

        # Inputs for Authority, Commanded Speed, Power, and Announcement
        authority_layout = QHBoxLayout()
        authority_layout.addWidget(QLabel("Authority (m):"))
        self.authority_input = QLineEdit()
        authority_layout.addWidget(self.authority_input)
        authority_button = QPushButton("Send")
        authority_layout.addWidget(authority_button)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Commanded Speed (mph):"))
        self.speed_input = QLineEdit()
        speed_layout.addWidget(self.speed_input)
        speed_button = QPushButton("Send")
        speed_layout.addWidget(speed_button)

        power_layout = QHBoxLayout()
        power_layout.addWidget(QLabel("Power Command (W):"))
        self.power_input = QLineEdit()
        power_layout.addWidget(self.power_input)
        power_button = QPushButton("Send")
        power_layout.addWidget(power_button)

        announcement_layout = QHBoxLayout()
        announcement_layout.addWidget(QLabel("Announcement:"))
        self.announcement_input = QLineEdit()
        announcement_layout.addWidget(self.announcement_input)
        announcement_button = QPushButton("Send")
        announcement_layout.addWidget(announcement_button)

        # Commanded Temperature and Service Brake
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(QLabel("Commanded Temperature (°F):"))
        self.temperature_input = QLineEdit()
        temperature_layout.addWidget(self.temperature_input)
        temperature_button = QPushButton("Send")
        temperature_layout.addWidget(temperature_button)

        brake_button = QPushButton("Service Brake")
        brake_button.setStyleSheet("background-color: red; color: white;")

        # Doors Control (Left and Right) and Lights (Headlights and Inside Lights)
        doors_lights_layout = QHBoxLayout()

        # Left Door Toggle
        left_door_layout = QVBoxLayout()
        left_door_layout.addWidget(QLabel("Left Door:"))
        self.left_door_open_button = self.create_toggle_button("Open", True)
        self.left_door_closed_button = self.create_toggle_button("Closed", False)
        left_door_layout.addWidget(self.left_door_open_button)
        left_door_layout.addWidget(self.left_door_closed_button)
        doors_lights_layout.addLayout(left_door_layout)

        # Right Door Toggle
        right_door_layout = QVBoxLayout()
        right_door_layout.addWidget(QLabel("Right Door:"))
        self.right_door_open_button = self.create_toggle_button("Open", True)
        self.right_door_closed_button = self.create_toggle_button("Closed", False)
        right_door_layout.addWidget(self.right_door_open_button)
        right_door_layout.addWidget(self.right_door_closed_button)
        doors_lights_layout.addLayout(right_door_layout)

        # Headlights Toggle
        headlights_layout = QVBoxLayout()
        headlights_layout.addWidget(QLabel("Headlights:"))
        self.headlights_on_button = self.create_toggle_button("On", True)
        self.headlights_off_button = self.create_toggle_button("Off", False)
        headlights_layout.addWidget(self.headlights_on_button)
        headlights_layout.addWidget(self.headlights_off_button)
        doors_lights_layout.addLayout(headlights_layout)

        # Inside Lights Toggle
        inside_lights_layout = QVBoxLayout()
        inside_lights_layout.addWidget(QLabel("Inside Lights:"))
        self.inside_lights_on_button = self.create_toggle_button("On", True)
        self.inside_lights_off_button = self.create_toggle_button("Off", False)
        inside_lights_layout.addWidget(self.inside_lights_on_button)
        inside_lights_layout.addWidget(self.inside_lights_off_button)
        doors_lights_layout.addLayout(inside_lights_layout)

        # Add all layouts to the main layout
        layout.addLayout(authority_layout)
        layout.addLayout(speed_layout)
        layout.addLayout(power_layout)
        layout.addLayout(announcement_layout)
        layout.addLayout(temperature_layout)
        layout.addWidget(brake_button)
        layout.addLayout(doors_lights_layout)

        self.setLayout(layout)

    def create_toggle_button(self, label_text, checked):
        """Create a toggle button with two states (on/off)."""
        button = QPushButton(label_text)
        button.setCheckable(True)
        button.setChecked(checked)
        button.setFixedSize(QSize(50, 30))
        button.setStyleSheet("background-color: green;" if checked else "background-color: gray;")
        button.clicked.connect(lambda: self.toggle_button_state(button))
        return button

    def toggle_button_state(self, button):
        """Toggle the button color between red (on) and green (off)."""
        if button.isChecked():
            button.setStyleSheet("background-color: green;")
        else:
            button.setStyleSheet("background-color: gray;")

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
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Train Control System")
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        main_layout = QHBoxLayout()

        # Create the tab widget
        self.tabs = QTabWidget()

        # Create pages
        select_train_page = SelectTrainPage()
        user_mode_page = UserModePage()
        test_bench_page = TestBenchPage()

        # Add tabs
        self.tabs.addTab(select_train_page, "Select a Train")
        self.tabs.addTab(user_mode_page, "User Mode")
        self.tabs.addTab(test_bench_page, "Testing")

        # Add tabs to the main layout
        main_layout.addWidget(self.tabs)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    #This function will update all other information in UI to match the train which was selected
    def index_changed(self, i): # i is an int which represent the index of the train
        print(f"Train {i} has been selected")

        self.current_train = i

        #update every widget in the UI
        #self.authority_widget.setText(f"  Authority: {train_list[i].authority} ft")
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

        #set kp and Ki values
        self.input_kp.setPlaceholderText(f"{train_list[i].k_p}")
        self.input_ki.setPlaceholderText(f"{train_list[i].k_i}")
        

        #check manual mode
        self.manual_mode()

        #check for errors
        self.check_errors()

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

        #activates door button again if in manual mode
        if train_list[self.current_train].manual_mode:
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

        #activates door button again if in manual mode
        if train_list[self.current_train].manual_mode:
            self.r_door_button.setEnabled(True)
            

    def check_errors(self):
        if train_list[self.current_train].failure_engine == True:
            self.engine_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
        else:
            self.engine_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
        if train_list[self.current_train].failure_brake == True:
            self.brake_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
        else:
            self.brake_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
        if train_list[self.current_train].failure_signal == True:
            self.signal_light.setStyleSheet("""
            background-color: red;
            border-radius: 25px;
            border: 2px solid black;
        """)
        else:
            self.signal_light.setStyleSheet("""
            background-color: gray;
            border-radius: 25px;
            border: 2px solid black;
        """)
            
    #handles when service brake is pressed
    def s_brake_pressed(self):
        train_list[self.current_train].s_brake = True

    #hands when emergency brake is clicked
    def e_brake_clicked(self):
        train_list[self.current_train].e_brake = True
        self.e_brake_button.setEnabled(False)

        #call the brake function to slow down train

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

