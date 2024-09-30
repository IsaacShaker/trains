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
        available_trains = ["Train 1", "Train 2", "Train 3", "Train 4"]

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select a Train:", font=QFont('Arial', 14)))

        # Create dropdown (combo box) for train selection
        self.train_dropdown = QComboBox()
        self.train_dropdown.addItems(available_trains)

        layout.addWidget(self.train_dropdown)

        self.setLayout(layout)


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

        # Add tabs
        self.tabs.addTab(select_train_page, "Select a Train")
        self.tabs.addTab(user_mode_page, "User Mode")
        self.tabs.addTab(QWidget(), "Testing")  # Placeholder for Testing tab

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

