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
from TrainModel.TrainModel import TrainModel
from TrainModel.TrainList import TrainList
# from TrainModel import TrainModel
# from TrainList import TrainList
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtCore import Qt

#train_list[1].atStation=False
#train_list[1].passCount=100
#train_list[1].update_passengers()

# train_list[1].numberOfCars=3
# train_list[1].calc_total_length()
# train_list[1].numberOfCars=4
# train_list[1].calc_total_length()

# train_list[1].serviceBrake=True
# train_list[1].limit_accel()
# train_list[1].serviceBrake=False
# train_list[1].emergencyBrake=True
# train_list[1].limit_accel()
# train_list[1].serviceBrake=True
# train_list[1].limit_accel()
# train_list[1].serviceBrake=False
# train_list[1].emergencyBrake=False
# train_list[1].currAccel=1
# train_list[1].limit_accel()

# train_list[1].currPower=0
# train_list[1].engineFailure=False
# train_list[1].currentVelocity=30
# #train_list[1].serviceBrake=True
# train_list[1].calc_total_mass()
# print(f"Current Mass: {train_list[1].totalMass}")
# print(f"Current Power: {train_list[1].currPower}")
# print(f"Engine Failure: {train_list[1].engineFailure}")
# print(f"Current Velocity: {train_list[1].currentVelocity}")
# train_list[1].receive_power()



class Train_UI(QMainWindow):
    def __init__(self, parent=None):
        super(Train_UI, self).__init__(parent)

        # Instantiate TrainList globally
        self.train_list = TrainList()

        self.train_list.add_train()
        self.train_list.add_train()
        self.train_list.add_train()

        self.setWindowTitle("Train Model")
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        main_layout = QHBoxLayout()

        # Create the tab widget
        self.tabs = QTabWidget()

        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #772ce8;
                padding: 5px;
            }
            QTabBar::tab {
                border: 2px solid #772ce8;
                padding: 10px;
                margin: 1px;
            }
            QTabBar::tab:selected {
                color: black;
                background-color: #f0f0ff;
                border-bottom-color: #772ce8;  /* Ensure no overlap between tabs */
            }
            QTabBar::tab:hover {
                background-color: #dcdcdc;
            }
        """)

        #Initialize
        select_train_page=QWidget()
        create_user_mode_page=QWidget()
        test_bench_page=QWidget()

        # Create pages
        # select_train_page = self.create_select_train_page()
        user_mode_page = self.create_user_mode_page()
        test_bench_page = self.create_test_bench_page()

        # Add tabs
        #self.tabs.addTab(select_train_page, "Select a Train")
        self.tabs.addTab(user_mode_page, "User Mode")
        self.tabs.addTab(test_bench_page, "Testing")

        # Add tabs to the main layout
        main_layout.addWidget(self.tabs)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.selected_train=self.train_list[0]
        self.train_select_update()

        # Connect the signal to the slot
        self.selected_train.temperature_changed.connect(self.update_temperature_label)
        self.selected_train.power_changed.connect(self.update_speeds_label)
        self.selected_train.passengers_changed.connect(self.update_beacon_label)
        self.selected_train.ui_refresh.connect(self.train_select_update)

    def create_user_mode_page(self):
        user_mode_widget = QWidget()

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the top section (Image)
        top_layout = QHBoxLayout()

        # Create a vertical layout for the train selection elements
        train_selection_layout = QVBoxLayout()

        # Add the selected train label
        self.selected_train_label = QLabel("Selected Train: 0")
        self.selected_train_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.selected_train_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        train_selection_layout.addWidget(self.selected_train_label)

        # Add instructions label below the selected train label
        # instructions_label = QLabel("Select a train and press 'Confirm' to select a new train.")
        # instructions_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # instructions_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        # train_selection_layout.addWidget(instructions_label)

        # Create the train dropdown
        self.train_dropdown = QComboBox()
        self.train_dropdown.setStyleSheet("font-size: 18px;")
        
        # Populate the dropdown with train names
        for i in range(len(self.train_list)):
            self.train_dropdown.addItem(f"Train {i}")

        # Connect the dropdown to the train_selected function
        self.train_dropdown.currentIndexChanged.connect(self.train_selected)
        train_selection_layout.addWidget(self.train_dropdown)

        # Create a button to confirm train selection
        select_train_button = QPushButton("Confirm Train Selection")
        select_train_button.setStyleSheet("""
            QPushButton {
                background-color: #772ce8;
                color: white;
                border: none;
                padding: 15px 20px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9e30ff;
            }
        """)
        select_train_button.clicked.connect(self.select_train)
        select_train_button.setFixedHeight(50)
        train_selection_layout.addWidget(select_train_button)

        # Add the train selection layout to the top layout (left side)
        top_layout.addLayout(train_selection_layout)

        # Add stretch to push content to the top-left
        train_selection_layout.addStretch()

        # Display an image using a relative path
        image_label = QLabel()
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'primantis.png')
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(250, 150, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Image not found.")
        image_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(image_label)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)

        # Announcement Label
        announcement_label = QLabel("Announcement:")
        announcement_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))  # Set font size for the announcement label
        self.announcement_text = QLabel("Stay clear of doors")
        self.announcement_text.setFont(QFont('Arial', 20, QFont.Weight.Bold))  # Set larger font for the announcement text
        self.announcement_text.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the announcement text
        main_layout.addWidget(announcement_label)
        main_layout.addWidget(self.announcement_text)

        # Emergency Brake Button (move it above the grids)
        self.emergency_brake_button = QPushButton("Emergency Brake")
        self.emergency_brake_button.setStyleSheet("background-color: red; color: white; font-size: 24px")
        self.emergency_brake_button.setFixedHeight(50)
        self.emergency_brake_button.clicked.connect(self.toggle_ebrake)
        main_layout.addWidget(self.emergency_brake_button)
        
        # Create a horizontal layout for left and right sections for group boxes
        horizontal_layout = QHBoxLayout()

        # Create left layout for Speed, Dimensions, and Train Status
        left_layout = QVBoxLayout()

        # Create right layout for Lights/Doors and Failure Modes
        right_layout = QVBoxLayout()

        #Velocity and acceleration grid
        speed_group_box = QGroupBox("Speed Information")
        speed_group_box.setStyleSheet("""
            QGroupBox {
                border: 3px solid #C0C0C0;
                border-radius: 8px;
                font-size:18px;
                padding: 6px;
            }
            QLabel {
                border: none;
                font-size:16px;
            }
        """)
        speed_group_box.setFixedHeight(100)  # Adjust the height as needed
        speed_layout = QVBoxLayout()

        # Velocity
        velocity_layout = QHBoxLayout()
        velocity_layout.addWidget(QLabel("Velocity (mph):"))
        self.velocity_label = QLabel("60")  # Change from button to QLabel
        velocity_layout.addWidget(self.velocity_label)
        speed_layout.addLayout(velocity_layout)

        # Acceleration
        acceleration_layout = QHBoxLayout()
        acceleration_layout.addWidget(QLabel("Acceleration (ft/s^2):"))
        self.acceleration_label = QLabel("2")  # Change from button to QLabel
        acceleration_layout.addWidget(self.acceleration_label)
        speed_layout.addLayout(acceleration_layout)

        speed_group_box.setLayout(speed_layout)

        # Add the Speed Information Group Box to the left layout
        left_layout.addWidget(speed_group_box)

        # Create and style Train Dimensions Group Box
        train_dimensions_group_box = QGroupBox("Train Dimensions")
        train_dimensions_layout = QVBoxLayout()

        # Length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Length (ft):"))
        self.length_label = QLabel("32.2")  # Change from button to QLabel
        length_layout.addWidget(self.length_label)
        train_dimensions_layout.addLayout(length_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width (ft):"))
        self.width_label = QLabel("2.65")  # Change from button to QLabel
        width_layout.addWidget(self.width_label)
        train_dimensions_layout.addLayout(width_layout)

        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height (ft):"))
        self.height_label = QLabel("3.42")  # Change from button to QLabel
        height_layout.addWidget(self.height_label)
        train_dimensions_layout.addLayout(height_layout)

        # Mass
        mass_layout = QHBoxLayout()
        mass_layout.addWidget(QLabel("Mass (tons):"))
        self.mass_label = QLabel("420")  # Change from button to QLabel
        mass_layout.addWidget(self.mass_label)
        train_dimensions_layout.addLayout(mass_layout)

        # Number of Cars
        num_cars_layout = QHBoxLayout()
        num_cars_layout.addWidget(QLabel("Number of Cars:"))
        self.num_cars_label = QLabel("1")  # Change from button to QLabel
        num_cars_layout.addWidget(self.num_cars_label)
        train_dimensions_layout.addLayout(num_cars_layout)

        train_dimensions_group_box.setLayout(train_dimensions_layout)

        # Create and style Train Status Group Box
        train_status_group_box = QGroupBox("Train Status")
        train_status_layout = QVBoxLayout()

        # Passenger Count
        passenger_count_layout = QHBoxLayout()
        passenger_count_layout.addWidget(QLabel("Passenger Count:"))
        self.passenger_count_label = QLabel("50")  # Change from button to QLabel
        passenger_count_layout.addWidget(self.passenger_count_label)
        train_status_layout.addLayout(passenger_count_layout)

        # Crew Count
        crew_count_layout = QHBoxLayout()
        crew_count_layout.addWidget(QLabel("Crew Count:"))
        self.crew_count_label = QLabel("2")  # Change from button to QLabel
        crew_count_layout.addWidget(self.crew_count_label)
        train_status_layout.addLayout(crew_count_layout)

        # Temperature
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(QLabel("Temperature (°F):"))
        self.temperature_label = QLabel("68")  # Change from button to QLabel
        temperature_layout.addWidget(self.temperature_label)
        train_status_layout.addLayout(temperature_layout)

        train_status_group_box.setLayout(train_status_layout)

        # Add group boxes to left layout
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
        right_door_layout.addWidget(self.right_door_label)
        doors_layout.addLayout(right_door_layout)

        # Left Door
        left_door_layout = QHBoxLayout()
        left_door_layout.addWidget(QLabel("Left Door:"))
        self.left_door_label = QLabel("Closed")  # Change from button to QLabel
        self.left_door_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the door state
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
        self.engine_button = QPushButton("Engine")
        self.brake_button = QPushButton("Brakes")
        self.signal_pickup_button = QPushButton("Signal Pickup")

        self.engine_button.clicked.connect(self.toggle_engine_failure)
        self.brake_button.clicked.connect(self.toggle_brake_failure)
        self.signal_pickup_button.clicked.connect(self.toggle_signal_pickup_failure)

        # Set styles for failure mode buttons
        for button in [self.engine_button, self.brake_button, self.signal_pickup_button]:
            button.setStyleSheet("background-color: red; color: white;") 

        failure_modes_layout.addWidget(self.engine_button)
        failure_modes_layout.addWidget(self.brake_button)
        failure_modes_layout.addWidget(self.signal_pickup_button)

        failure_modes_group_box.setLayout(failure_modes_layout)
        right_layout.addWidget(failure_modes_group_box)

        # Add left and right layouts to horizontal layout
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(right_layout)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Set the main layout to the user mode widget
        user_mode_widget.setLayout(main_layout)
        return user_mode_widget


    def toggle_ebrake(self):
        emergencyBrakeTemp = not self.selected_train.emergencyBrake
        self.selected_train.set_emergencyBrake(emergencyBrakeTemp)

    def toggle_engine_failure(self):
        engineFailureTemp = not self.selected_train.engineFailure
        self.selected_train.set_engine_failure(engineFailureTemp)

    def toggle_brake_failure(self):
        brakeFailureTemp = not self.selected_train.brakeFailure
        self.selected_train.set_brake_failure(brakeFailureTemp)

    def toggle_signal_pickup_failure(self):
        signalPickupFailureTemp = not self.selected_train.signalPickupFailure
        self.selected_train.set_signal_pickup_failure(signalPickupFailureTemp)

    def update_ebrake_button(self):
        if self.selected_train.emergencyBrake:
            self.emergency_brake_button.setText("Emergency Brake Pulled")
            self.emergency_brake_button.setStyleSheet("background-color: darkred; color: white; font-size: 24px ")  # Darker shade for failure
        else:
            self.emergency_brake_button.setText("Emergency Brake")
            self.emergency_brake_button.setStyleSheet("background-color: red; color: white; font-size: 24px")

    def apply_service_brake(self):
        # Apply the brake
        self.selected_train.serviceBrake = True
        self.service_brake_button.setText("Brakes applied")
        print("Brakes applied.")

    def release_service_brake(self):
        # Release the brake
        self.selected_train.serviceBrake = False
        self.service_brake_button.setText("Service Brake")
        print("Brakes released.")

    def toggle_service_brake(self):
        if self.selected_train.serviceBrake:
            self.release_service_brake()  # If the brake is applied, release it
            self.toggle_brake_button.setText("Apply Service Brake")  # Change button text
        else:
            self.apply_service_brake()  # If the brake is not applied, apply it
            self.toggle_brake_button.setText("Release Service Brake")  # Change button text

    def update_failure_mode_button(self):
        if self.selected_train.engineFailure:
            self.engine_button.setText("Engine Failed")
            self.engine_button.setStyleSheet("background-color: darkred; color: white;")  # Darker shade for failure
        else:
            self.engine_button.setText("Engine")
            self.engine_button.setStyleSheet("background-color: red; color: white;")
        
        if self.selected_train.signalPickupFailure:
            self.signal_pickup_button.setText("Signal Pickup Failed")
            self.signal_pickup_button.setStyleSheet("background-color: darkred; color: white;")
        else:
            self.signal_pickup_button.setText("Signal Pickup")
            self.signal_pickup_button.setStyleSheet("background-color: red; color: white;")

        if self.selected_train.brakeFailure:
            self.brake_button.setText("Brakes Failed")
            self.brake_button.setStyleSheet("background-color: darkred; color: white;")
        else:
            self.brake_button.setText("Brakes")
            self.brake_button.setStyleSheet("background-color: red; color: white;")

    def toggle_headlights_state(self):
        self.selected_train.headLights = not self.selected_train.headLights
        self.update_lights_state()

    def update_lights_state(self):
        self.headlights_label.setText("On" if self.selected_train.headLights else "Off")
        self.headlights_label.setStyleSheet("background-color: yellow; color:black" if self.selected_train.headLights else "background-color: gray; color:white")
        self.inside_lights_label.setText("On" if self.selected_train.insideLights else "Off")
        self.inside_lights_label.setStyleSheet("background-color: yellow; color:black" if self.selected_train.insideLights else "background-color: gray; color:white")

    def toggle_inside_lights_state(self):
        self.selected_train.insideLights = not self.selected_train.insideLights
        self.update_lights_state()

    def toggle_left_door_state(self):
        self.selected_train.leftDoor = not self.selected_train.leftDoor
        self.update_door_states()

    def toggle_right_door_state(self):
        self.selected_train.rightDoor = not self.selected_train.rightDoor
        self.update_door_states()

    def update_door_states(self):
        self.right_door_label.setText("Open" if self.selected_train.rightDoor else "Closed")
        self.right_door_label.setStyleSheet("background-color: green;" if self.selected_train.rightDoor else "background-color: red;")
        
        self.left_door_label.setText("Open" if self.selected_train.leftDoor else "Closed")
        self.left_door_label.setStyleSheet("background-color: green;" if self.selected_train.leftDoor else "background-color: red;")

    def create_test_bench_page(self):
        test_bench_widget = QWidget()

        # Main layout for the Test Bench
        layout = QVBoxLayout()

        # Add centered text at the top
        instruction_label = QLabel("Enter an input and press send to enter")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        instruction_label.setContentsMargins(0, 10, 0, 10)  # Reduce space around the label
        layout.addWidget(instruction_label)

        # Inputs for Authority, Commanded Speed, Power, and Announcement
        authority_layout = QHBoxLayout()
        authority_layout.addWidget(QLabel("Authority (m):"))
        self.authority_input = QLineEdit()
        authority_layout.addWidget(self.authority_input)
        authority_button = QPushButton("Send")
        authority_button.setStyleSheet("background-color: #772ce8; color: white;")
        authority_button.clicked.connect(self.send_authority)
        authority_layout.addWidget(authority_button)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Commanded Speed (km/hr):"))
        self.speed_input = QLineEdit()
        speed_layout.addWidget(self.speed_input)
        speed_button = QPushButton("Send")
        speed_button.setStyleSheet("background-color: #772ce8; color: white;")
        speed_button.clicked.connect(self.send_commanded_speed)
        speed_layout.addWidget(speed_button)

        power_layout = QHBoxLayout()
        power_layout.addWidget(QLabel("Power Command (W):"))
        self.power_input = QLineEdit()
        power_layout.addWidget(self.power_input)
        power_button = QPushButton("Send")
        power_button.setStyleSheet("background-color: #772ce8; color: white;")
        power_button.clicked.connect(self.send_power)
        power_layout.addWidget(power_button)

        announcement_layout = QHBoxLayout()
        announcement_layout.addWidget(QLabel("Announcement:"))
        self.announcement_input = QLineEdit()
        announcement_layout.addWidget(self.announcement_input)
        announcement_button = QPushButton("Send")
        announcement_button.setStyleSheet("background-color: #772ce8; color: white;")
        announcement_button.clicked.connect(self.send_announcement)
        announcement_layout.addWidget(announcement_button)

        # Commanded Temperature
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(QLabel("Commanded Temperature (°F):"))
        self.temperature_input = QLineEdit()
        temperature_layout.addWidget(self.temperature_input)
        temperature_button = QPushButton("Send")
        temperature_button.setStyleSheet("background-color: #772ce8; color: white;")
        temperature_button.clicked.connect(self.send_temperature)
        temperature_layout.addWidget(temperature_button)

        # Add all input layouts to the main layout
        layout.addLayout(authority_layout)
        layout.addLayout(speed_layout)
        layout.addLayout(power_layout)
        layout.addLayout(announcement_layout)
        layout.addLayout(temperature_layout)

        # Doors Control (Left) and Lights Control (Right)
        doors_lights_layout = QHBoxLayout()

        # Left: Doors Toggle
        doors_layout = QVBoxLayout()
        doors_layout.addWidget(QLabel("Doors:"))

        self.right_door_button = QPushButton("Toggle Right Door")
        self.right_door_button.setCheckable(False)
        self.right_door_button.clicked.connect(self.toggle_right_door_state)
        doors_layout.addWidget(self.right_door_button)

        self.left_door_button = QPushButton("Toggle Left Door")
        self.left_door_button.setCheckable(False)
        self.left_door_button.clicked.connect(self.toggle_left_door_state)
        doors_layout.addWidget(self.left_door_button)

        doors_lights_layout.addLayout(doors_layout)

        # Right: Lights Toggle
        lights_layout = QVBoxLayout()
        lights_layout.addWidget(QLabel("Lights:"))

        self.headlights_button = QPushButton("Toggle Headlights")
        self.headlights_button.setCheckable(False)
        self.headlights_button.clicked.connect(self.toggle_headlights_state)
        lights_layout.addWidget(self.headlights_button)

        self.inside_lights_button = QPushButton("Toggle Inside Lights")
        self.inside_lights_button.setCheckable(False)
        self.inside_lights_button.clicked.connect(self.toggle_inside_lights_state)
        lights_layout.addWidget(self.inside_lights_button)

        doors_lights_layout.addLayout(lights_layout)

        # Add doors and lights layout below the brake button
        layout.addLayout(doors_lights_layout)

        # Service Brake Button
        self.service_brake_button = QPushButton("Service Brake")
        self.service_brake_button.setFixedSize(100, 80) 
        self.service_brake_button.setStyleSheet("""
        QPushButton {
            background-color: yellow; 
            color: black;
        }
        QPushButton:pressed {
            background-color: darkgoldenrod;  /* Darker shade when pressed */
            color: black;
        }
        """)
        # Connect mouse events
        self.service_brake_button.pressed.connect(self.apply_service_brake)
        self.service_brake_button.released.connect(self.release_service_brake)

        # Beacon Info Button (Styled Purple)
        self.beacon_info_button = QPushButton("Send Beacon Info")
        self.beacon_info_button.setStyleSheet("background-color: #772ce8; color: white;")
        self.beacon_info_button.setFixedSize(100, 80)
        self.beacon_info_button.clicked.connect(self.send_beacon_info)

        # Create the toggle button
        self.toggle_brake_button = QPushButton("Toggle Service Brake")
        self.toggle_brake_button.setStyleSheet("background-color: #772ce8; color: white;")

        # Connect the button's click event to the toggle function
        self.toggle_brake_button.clicked.connect(self.toggle_service_brake)

        # Layout for Service Brake, Beacon Info, and Toggle Service Brake buttons
        bottom_layout = QVBoxLayout()  # Changed to QVBoxLayout to stack the buttons
        button_row_layout = QHBoxLayout()  # Add a row layout for service brake and beacon
        button_row_layout.addWidget(self.service_brake_button)
        button_row_layout.addWidget(self.beacon_info_button)
        
        bottom_layout.addLayout(button_row_layout)  # Add the row layout to the bottom layout
        bottom_layout.addWidget(self.toggle_brake_button)  # Add the toggle button below

        layout.addLayout(bottom_layout)

        test_bench_widget.setLayout(layout)
        return test_bench_widget

    #Function to send our beacon info
    def send_beacon_info(self):
        print("SEND BEACON")
        self.selected_train.set_beaconInfo("b1,2,lebron")

    def update_beacon_label(self):
        self.passenger_count_label.setText(f"{self.selected_train.passCount}")  # Update the UI label with new temperature
        self.mass_label.setText(f"{self.selected_train.totalMass:.2f}")
        self.announcement_text.setText(self.selected_train.announcements)

        # Open the right doors
        self.toggle_right_door_state()

        # Close the right doors after 10 seconds using a QTimer
        QTimer.singleShot(10000, lambda: self.toggle_right_door_state())  # 10,000 milliseconds = 10 seconds

    # Function to handle authority input
    def send_authority(self):
        authority_value = self.authority_input.text()
        if authority_value.isdigit():  # Simple validation
            self.selected_train.set_authority(float(authority_value))
            self.authority_input.clear()
        else:
            print("Invalid Authority value")

    # Function to handle commanded speed input
    def send_commanded_speed(self):
        speed_value = self.speed_input.text()
        try:
            speed = float(speed_value)
            self.selected_train.set_commandedSpeed(speed)
            print(f"Commanded speed set to {self.selected_train.commandedSpeed} mph.")
            self.speed_input.clear()
        except ValueError:
            print("Invalid Speed value")

    # Function to handle power input
    def send_power(self):
        power_value = self.power_input.text()
        try:
            power = float(power_value)
            self.selected_train.set_commanded_power(power)
        except ValueError:
            print("Invalid Power value")

    def update_speeds_label(self):
        self.velocity_label.setText(f"{self.selected_train.mps_to_mph(self.selected_train.currentVelocity):.2f}")
        self.acceleration_label.setText(f"{self.selected_train.m_to_ft(self.selected_train.currAccel):.2f}")

    # Function to handle announcement input
    def send_announcement(self):
        announcement = self.announcement_input.text()
        self.selected_train.set_announcements(announcement)
        self.announcement_input.clear()

    # Function to handle temperature input
    def send_temperature(self):
        temperature_value = self.temperature_input.text()
        try:
            temperature = float(temperature_value)
            self.selected_train.set_commandedTemperature(temperature)
            print(f"Temperature set to {self.selected_train.commandedTemperature} °F.")
            self.temperature_input.clear()
        except ValueError:
            print("Invalid Temperature value")

    def update_temperature_label(self):
        self.temperature_label.setText(f"{self.selected_train.temperature:.2f}")  # Update the UI label with new temperature

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

    def train_selected(self):
        selected_index = self.train_dropdown.currentIndex()

    def select_train(self):
        selected_index = self.train_dropdown.currentIndex()
        self.selected_train = self.train_list[selected_index]
        self.selected_train.ID=selected_index
        self.train_select_update()

    def train_select_update(self):
        # Convert float values to strings before setting the text
        self.selected_train_label.setText(f"Selected Train: {self.selected_train.ID}")
        self.velocity_label.setText(f"{self.selected_train.mps_to_mph(self.selected_train.currentVelocity):.2f}")
        self.acceleration_label.setText(f"{self.selected_train.m_to_ft(self.selected_train.currAccel):.2f}")

        self.update_lights_state()
        self.update_door_states()
        self.update_failure_mode_button()
        self.update_ebrake_button()

        self.announcement_text.setText(f"{self.selected_train.announcements}")

        self.height_label.setText(f"{self.selected_train.m_to_ft(self.selected_train.trainHeight):.2f}")
        self.width_label.setText(f"{self.selected_train.m_to_ft(self.selected_train.trainWidth):.2f}")
        self.length_label.setText(f"{self.selected_train.m_to_ft(self.selected_train.trainLength):.2f}")
        self.mass_label.setText(str(self.selected_train.totalMass))
        self.num_cars_label.setText(str(self.selected_train.numberOfCars))
        
        self.temperature_label.setText(f"{self.selected_train.temperature:.2f}")
        self.crew_count_label.setText(str(self.selected_train.crewCount))
        self.passenger_count_label.setText(str(self.selected_train.passCount))


# Run the application
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    main_window = Train_UI()
    main_window.show()
    sys.exit(app.exec())
