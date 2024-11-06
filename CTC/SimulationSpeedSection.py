import time
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QComboBox, QFrame
from PyQt6.QtCore import Qt, QTimer

class SimulationSpeedSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       
        # Create Simulation Speed Section layout
        self.layout = QHBoxLayout()
        self.speed_label = QLabel("Simulation Speed")
        self.speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.speed_label.setStyleSheet("color: white; font-size: 20px;")
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.speed_label)

        # Vertical layout for Clock and Simulation Speed
        sim_layout = QVBoxLayout()

        # Add the clock label
        self.clock_label = QLabel("00:00:00")
        self.clock_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setStyleSheet("color: white; font-size: 18px;")
        sim_layout.addWidget(self.clock_label)

        # Horizontal Layout for on/off button and sim speed combo box
        simOptions_layout = QHBoxLayout()

        # Create a QComboBox for simulation speed
        self.speed_combo_box = QComboBox()
        self.speed_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.speed_combo_box.setStyleSheet("color: white; background-color: #772CE8;")
        self.speed_combo_box.addItems(["1x", "10x", "50x"])
        simOptions_layout.addWidget(self.speed_combo_box)

        # Create on/off button for the simulation
        self.operational_button = QPushButton("Start")
        self.operational_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.operational_button.setStyleSheet("background-color: green; color: white;")
        simOptions_layout.addWidget(self.operational_button)

        # Add the horizontal layout to the sim_layout
        sim_layout.addLayout(simOptions_layout)

        # Add the vertical layout to the main layout
        self.layout.addLayout(sim_layout)
        self.setLayout(self.layout)

        # Connect button signals if needed
        self.operational_button.clicked.connect(self.operationalClicked)

    # Make all frames of widgets consistent
    def create_section_frame(self, width=None, height=None):
        """Helper function to create a QFrame with consistent styling and size."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        frame.setStyleSheet("border: 2px solid #772CE8;")
        # Set minimum size if provided
        if width and height:
            frame.setMinimumSize(width, height)  # Set minimum size
        return frame

    # The functionality of the user selecting the Simulation Speed of the system
    def simSpeedSelected(self, s):
        print("The simulation is now running at", s, "speed!")
        self.speed = int(s[:-1])  # Extracting the numeric value from the selected string

    # The functionality of the user starting the simulation
    def operationalClicked(self):
        # Toggle the simulation state
        if not self.simulationRunning:
            self.simulationRunning = True
            self.start_time = time.time()  # Reset start time when simulation starts
            print("The simulation has started!")
        else:
            self.simulationRunning = False
            print("The simulation has been stopped!")

        # Update the button text to reflect the current state
        sender = self.sender()  # Get the button that triggered the event
        if self.simulationRunning:
            sender.setText("Stop")  # Change the button text to "Stop" when running
            sender.setStyleSheet("background-color: red; color: white;")
        else:
            sender.setText("Start")  # Change the button text back to "Start" when stopped
            sender.setStyleSheet("background-color: green; color: white;")

    def format_time(self, seconds: int) -> str:
        hours = (seconds // 3600) % 24
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def update_clock(self):
        # Only update the clock if the simulation is running
        if self.simulationRunning:
            # Update the time according to the previous time and the simulation speed
            self.newTime = self.oldTime + (1 * self.speed)

            # Update the clock label with the formatted time
            formatted_time = self.format_time(self.newTime)
            self.clock_label.setText(formatted_time)

            # Update oldTime to the newTime for the next call
            self.oldTime = self.newTime