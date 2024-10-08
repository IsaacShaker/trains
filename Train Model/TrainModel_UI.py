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
from TrainModel import TrainModel
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt

# Define train_list globally
train_list = []

def addTrain(): 
    new_train = TrainModel()
    train_list.append(new_train)

# Call addTrain to populate the list
addTrain()
addTrain()
addTrain()

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



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

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
        select_train_page = self.create_select_train_page()
        user_mode_page = self.create_user_mode_page()
        test_bench_page = self.create_test_bench_page()

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

    def create_user_mode_page(self):
        user_mode_widget=QWidget()

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the top section (Image)
        top_layout = QHBoxLayout()

        # Display an image using a relative path
        image_label = QLabel()
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'dlc.png')
        pixmap = QPixmap(image_path).scaled(700, 150, Qt.AspectRatioMode.KeepAspectRatio)  # Adjust size as needed
        image_label.setPixmap(pixmap)
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
        self.velocity_label = QLabel("60 mph")  # Change from button to QLabel
        velocity_layout.addWidget(self.velocity_label)
        speed_layout.addLayout(velocity_layout)

        # Acceleration
        acceleration_layout = QHBoxLayout()
        acceleration_layout.addWidget(QLabel("Acceleration:"))
        self.acceleration_label = QLabel("2 ft/s^2")  # Change from button to QLabel
        acceleration_layout.addWidget(self.acceleration_label)
        speed_layout.addLayout(acceleration_layout)

        speed_group_box.setLayout(speed_layout)

        # Create and style Train Dimensions Group Box
        train_dimensions_group_box = QGroupBox("Train Dimensions")
        train_dimensions_layout = QVBoxLayout()

        # Length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Length:"))
        self.length_label = QLabel("105.6 ft")  # Change from button to QLabel
        length_layout.addWidget(self.length_label)
        train_dimensions_layout.addLayout(length_layout)

        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        self.width_label = QLabel("8.6 ft")  # Change from button to QLabel
        width_layout.addWidget(self.width_label)
        train_dimensions_layout.addLayout(width_layout)

        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_label = QLabel("11.2 ft")  # Change from button to QLabel
        height_layout.addWidget(self.height_label)
        train_dimensions_layout.addLayout(height_layout)

        # Mass
        mass_layout = QHBoxLayout()
        mass_layout.addWidget(QLabel("Mass:"))
        self.mass_label = QLabel("90,000 lbs")  # Change from button to QLabel
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
        temperature_layout.addWidget(QLabel("Temperature:"))
        self.temperature_label = QLabel("68 °F")  # Change from button to QLabel
        temperature_layout.addWidget(self.temperature_label)
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

        user_mode_widget.setLayout(main_layout)
        return user_mode_widget

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

    def create_select_train_page(self):
        # Create a widget for the Select Train page
        select_train_widget = QWidget()
        layout = QVBoxLayout()

        # Add a label to display the currently selected train
        selected_train_label = QLabel("Selected Train: None")
        selected_train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_train_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(selected_train_label)

        # Add instructions label below the selected train label
        instructions_label = QLabel("Select a train and press 'Confirm' to select a new train.")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        layout.addWidget(instructions_label)

        self.train_dropdown = QComboBox()  # Make this an instance variable
        self.train_dropdown.setStyleSheet("font-size: 18px;") 

        # Create a dropdown for available trains
        for i in range(len(train_list)):
            self.train_dropdown.addItem(f"Train {i}")  # Update dropdown with train names

        # Connect the dropdown selection to the train_selected function
        self.train_dropdown.currentIndexChanged.connect(self.train_selected)

        layout.addWidget(self.train_dropdown)

        # Button to confirm selection with improved styling
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
        select_train_button.clicked.connect(self.select_train)  # Connect button to selection logic
        layout.addWidget(select_train_button)

        layout.addStretch()
        select_train_widget.setLayout(layout)
        return select_train_widget

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
        authority_layout.addWidget(authority_button)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Commanded Speed (mph):"))
        self.speed_input = QLineEdit()
        speed_layout.addWidget(self.speed_input)
        speed_button = QPushButton("Send")
        speed_button.setStyleSheet("background-color: #772ce8; color: white;")
        speed_layout.addWidget(speed_button)

        power_layout = QHBoxLayout()
        power_layout.addWidget(QLabel("Power Command (W):"))
        self.power_input = QLineEdit()
        power_layout.addWidget(self.power_input)
        power_button = QPushButton("Send")
        power_button.setStyleSheet("background-color: #772ce8; color: white;")
        power_layout.addWidget(power_button)

        announcement_layout = QHBoxLayout()
        announcement_layout.addWidget(QLabel("Announcement:"))
        self.announcement_input = QLineEdit()
        announcement_layout.addWidget(self.announcement_input)
        announcement_button = QPushButton("Send")
        announcement_button.setStyleSheet("background-color: #772ce8; color: white;")
        announcement_layout.addWidget(announcement_button)

        # Commanded Temperature
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(QLabel("Commanded Temperature (°F):"))
        self.temperature_input = QLineEdit()
        temperature_layout.addWidget(self.temperature_input)
        temperature_button = QPushButton("Send")
        temperature_button.setStyleSheet("background-color: #772ce8; color: white;")
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

        self.left_door_button = QPushButton("Open Left Door")
        self.left_door_button.setCheckable(True)
        doors_layout.addWidget(self.left_door_button)

        self.right_door_button = QPushButton("Open Right Door")
        self.right_door_button.setCheckable(True)
        doors_layout.addWidget(self.right_door_button)

        doors_lights_layout.addLayout(doors_layout)

        # Right: Lights Toggle
        lights_layout = QVBoxLayout()
        lights_layout.addWidget(QLabel("Lights:"))

        self.headlights_button = QPushButton("Turn On Headlights")
        self.headlights_button.setCheckable(True)
        lights_layout.addWidget(self.headlights_button)

        self.inside_lights_button = QPushButton("Turn On Inside Lights")
        self.inside_lights_button.setCheckable(True)
        lights_layout.addWidget(self.inside_lights_button)

        doors_lights_layout.addLayout(lights_layout)

        # Add doors and lights layout below the brake button
        layout.addLayout(doors_lights_layout)

        # Service Brake Button (below inputs but above doors/lights)
        brake_button = QPushButton("Service Brake")
        brake_button.setFixedSize(100, 80)  # Make it less wide and taller
        brake_button.setStyleSheet("background-color: yellow; color: black;")
        layout.addWidget(brake_button, alignment=Qt.AlignmentFlag.AlignCenter)

        test_bench_widget.setLayout(layout)
        return test_bench_widget


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
        """Handle train selection change."""
        selected_index = self.train_dropdown.currentIndex()

    def select_train(self):
        selected_index = self.train_dropdown.currentIndex()
        selected_train = train_list[selected_index]
        self.train_select_update(selected_train)

    def train_select_update(self, selected_train):
        # Convert float values to strings before setting the text
        self.velocity_label.setText(str(selected_train.currentVelocity))
        self.acceleration_label.setText(str(selected_train.currAccel))
        
        self.update_headlights_state(selected_train.headLights)
        self.update_inside_lights_state(selected_train.insideLights)
        self.update_door_states(selected_train.rightDoor, selected_train.leftDoor)
        
        self.height_label.setText(str(selected_train.trainHeight))
        self.width_label.setText(str(selected_train.trainWidth))
        self.length_label.setText(str(selected_train.trainLength))
        self.mass_label.setText(str(selected_train.totalMass))
        self.num_cars_label.setText(str(selected_train.numberOfCars))
        
        self.temperature_label.setText(str(selected_train.temperature))
        self.crew_count_label.setText(str(selected_train.crewCount))
        self.passenger_count_label.setText(str(selected_train.passCount))


# Run the application
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
