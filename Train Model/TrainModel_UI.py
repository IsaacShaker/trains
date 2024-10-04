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
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize


class UserModePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Announcement: Stay clear of doors"))

        # Display an image using a relative path
        image_label = QLabel()

        # Construct the relative path for the image
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'kennywood_ad.jpg')
        pixmap = QPixmap(image_path)  # Load the image
        image_label.setPixmap(pixmap.scaled(30, 30))  # Adjust the size as needed
        

        # Speed Information
        speed_layout = QVBoxLayout()
        speed_layout.addWidget(QLabel("Speed", font=QFont('Arial', 14)))
        speed_layout.addWidget(QLabel("Velocity: 60 mph"))
        speed_layout.addWidget(QLabel("Acceleration: 2 feet/s²"))

        # Train Dimensions
        train_dimensions_layout = QVBoxLayout()
        train_dimensions_layout.addWidget(QLabel("Train Dimensions", font=QFont('Arial', 14)))
        train_dimensions_layout.addWidget(QLabel("Length: 105.6 ft"))
        train_dimensions_layout.addWidget(QLabel("Width: 8.6 ft"))
        train_dimensions_layout.addWidget(QLabel("Height: 11.2 ft"))
        train_dimensions_layout.addWidget(QLabel("Mass: 90,000 lbs"))
        train_dimensions_layout.addWidget(QLabel("Number of Cars: 1"))

        # Emergency Brake Button
        emergency_brake_button = QPushButton("Emergency Brake")

        # Lights and Doors - Labels with toggle buttons
        lights_doors_layout = QVBoxLayout()
        lights_doors_layout.addWidget(QLabel("Lights/Doors", font=QFont('Arial', 14)))

        # Right Door
        right_door_layout = QHBoxLayout()
        right_door_layout.addWidget(QLabel("Right Door:"))
        self.right_door_button = self.create_toggle_button("Right Door")
        right_door_layout.addWidget(self.right_door_button)

        # Left Door
        left_door_layout = QHBoxLayout()
        left_door_layout.addWidget(QLabel("Left Door:"))
        self.left_door_button = self.create_toggle_button("Left Door")
        left_door_layout.addWidget(self.left_door_button)

        # Headlights
        headlights_layout = QHBoxLayout()
        headlights_layout.addWidget(QLabel("Headlights:"))
        self.headlights_button = self.create_toggle_button("Headlights")
        headlights_layout.addWidget(self.headlights_button)

        # Inside Lights
        inside_lights_layout = QHBoxLayout()
        inside_lights_layout.addWidget(QLabel("Inside Lights:"))
        self.inside_lights_button = self.create_toggle_button("Inside Lights")
        inside_lights_layout.addWidget(self.inside_lights_button)

        # Add light/door layouts
        lights_doors_layout.addLayout(right_door_layout)
        lights_doors_layout.addLayout(left_door_layout)
        lights_doors_layout.addLayout(headlights_layout)
        lights_doors_layout.addLayout(inside_lights_layout)

        # Train Status
        train_status_layout = QVBoxLayout()
        train_status_layout.addWidget(QLabel("Train Status", font=QFont('Arial', 14)))
        train_status_layout.addWidget(QLabel("Passenger Count: 50"))
        train_status_layout.addWidget(QLabel("Crew Count: 2"))
        train_status_layout.addWidget(QLabel("Temperature: 68 °F"))

        # Control Buttons for Engine, Brake, and Signal Pickup
        control_buttons_layout = QHBoxLayout()
        engine_button = QPushButton("Engine")
        brake_button = QPushButton("Brake")
        signal_pickup_button = QPushButton("Signal Pickup")

        control_buttons_layout.addWidget(engine_button)
        control_buttons_layout.addWidget(brake_button)
        control_buttons_layout.addWidget(signal_pickup_button)

        # Failure Modes Section
        failure_modes_layout = QVBoxLayout()
        failure_modes_layout.addWidget(QLabel("Failure Modes", font=QFont('Arial', 14)))
        failure_modes_layout.addLayout(control_buttons_layout)

        # Combine all layouts
        layout.addLayout(speed_layout)
        layout.addWidget(image_label)
        layout.addLayout(train_dimensions_layout)
        layout.addWidget(emergency_brake_button)
        layout.addLayout(lights_doors_layout)
        layout.addLayout(failure_modes_layout)
        layout.addLayout(train_status_layout)

        self.setLayout(layout)

    def create_toggle_button(self, label_text):
        """Create a toggle button that switches between red (on) and green (off)."""
        button = QPushButton()
        button.setCheckable(True)
        button.setFixedSize(QSize(50, 30))  # Set size for the button
        button.setStyleSheet("background-color: green")  # Start with 'off' state (green)
        button.clicked.connect(lambda checked, btn=button: self.toggle_button(btn))
        return button

    def toggle_button(self, button):
        """Toggle the button color between red (on) and green (off)."""
        if button.isChecked():
            button.setStyleSheet("background-color: red")
        else:
            button.setStyleSheet("background-color: green")


class SelectTrainPage(QWidget):
    def __init__(self):
        super().__init__()

        # List of available trains
        available_trains = ["Train 0", "Train 1", "Train 2", "Train 3"]

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select a Train:", font=QFont('Arial', 14)))

        # Create dropdown (combo box) for train selection
        self.train_dropdown = QComboBox()
        self.train_dropdown.addItems(available_trains)

        layout.addWidget(self.train_dropdown)

        self.setLayout(layout)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

