import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QInputDialog, QDialog, QLineEdit
from PyQt6.QtCore import Qt, QTimer

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulationRunning = False #this is necessary for clock to work properly

        self.oldTime = 21600 # the system will began at 6AM
        self.speed = 1

        # create the open block list, everything should open upon creation
        self.open_blocks = []
        for i in range(1,16): # fill the list with all necesary blocks
            self.open_blocks.append(('Blue',i))

        # create the maintenance blocks list
        self.maintenance_blocks = []

        #create the occupied block list
        self.occupied_blocks = []

        # Set the window title
        self.setWindowTitle("CTC Office")

        # Set a fixed size for the window
        self.setFixedSize(850, 875)  # Width: 850, Height: 875

        # Set the background color of the window using a color code
        self.setStyleSheet("background-color: #171717;")  # Dark background

        # Create the tab widget and set it as the central widget of the window
        self.tab_widget = QTabWidget()

        # Style the tab buttons
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #171717;  /* Tab button background color */
                color: white;         /* Tab button text color */
                padding: 10px;        /* Padding inside the tab */
                border: 1px solid #FFFFFF; /* Border color */
                border-bottom: none;  /* No border at the bottom */
            }
            QTabBar::tab:selected {
                background: #772CE8;  /* Background color for the selected tab */
                color: white;         /* Text color of the selected tab */
            }
        """)

        self.setCentralWidget(self.tab_widget)

        # Add the tabs to the tab widget
        self.create_tabs()

        # Timer for clock update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)

        # Initialize the start time, speed, and total elapsed time
        self.start_time = time.time()
        self.speed = 1
        self.total_elapsed_time = 0  # New variable to keep track of total elapsed time
        self.timer.start(1000)  # Update every second

    def create_tabs(self):
        # Home Tab content
        home = QWidget()
        home_layout = QVBoxLayout()

        # Call the layout with frames to organize the UI for Home tab
        self.create_home_layout(home_layout)

        home.setLayout(home_layout)
        home.setStyleSheet("background-color: #171717;")  # Black background

        # Test Bench Tab content
        test_bench = QWidget()
        test_bench_layout = QVBoxLayout()

        # Add a placeholder for Test Bench
        test_bench_label = QLabel("Test Bench content goes here.")
        test_bench_label.setStyleSheet("color: white; font-size: 18px;")
        test_bench_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        test_bench_layout.addWidget(test_bench_label)

        test_bench.setLayout(test_bench_layout)
        test_bench.setStyleSheet("background-color: #171717;")  # Black background

        # Add the tabs to the tab widget
        self.tab_widget.addTab(home, "Home")
        self.tab_widget.addTab(test_bench, "Test Bench")

    def create_home_layout(self, layout):
        # Main layout grid for Home tab
        grid_layout = QGridLayout()

        # Set the layout margins and spacing
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed
        grid_layout.setSpacing(10)  # Adjust spacing between widgets

        # 1. Maintenance Section (Top left)
        maintenance_frame = self.create_section_frame(400, 80)  # Reduced height
        maintenance_layout = QHBoxLayout()
        maintenance_label = QLabel("Maintenance")
        maintenance_label.setStyleSheet("color: white; font-size: 18px;")
        maintenance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        maintenance_layout.addWidget(maintenance_label)

        # Vertical layout for Closure and Opening buttons
        button_layout = QVBoxLayout()
        
        # Define Maintenance Closure button
        closure_button = QPushButton("Closure")
        closure_button.setStyleSheet("background-color: yellow; color: black;")
        closure_button.clicked.connect(self.closureClicked)
        button_layout.addWidget(closure_button)  # Add the Closure button to the horizontal layout
        
        # Define Maintenance Opening button
        opening_button = QPushButton("Opening")
        opening_button.setStyleSheet("background-color: green; color: black;")
        opening_button.clicked.connect(self.openingClicked)
        button_layout.addWidget(opening_button)  # Add the Opening button to the horizontal layout

        maintenance_layout.addLayout(button_layout)  # Add the horizontal button layout to the maintenance frame layout
        maintenance_frame.setLayout(maintenance_layout)
        grid_layout.addWidget(maintenance_frame, 0, 0)

        # 2. Simulation Speed Section (Top right)
        speed_frame = self.create_section_frame(400, 80)  # Reduced height
        speed_layout = QHBoxLayout()  # Using QHBoxLayout to align items horizontally
        speed_label = QLabel("Simulation Speed")
        speed_label.setStyleSheet("color: white; font-size: 18px;")
        speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        speed_layout.addWidget(speed_label)

        # Vertical layout for Clock and Simulation Speed
        sim_layout = QVBoxLayout()

        # Add the clock label
        self.clock_label = QLabel(self.format_time(0))
        self.clock_label.setStyleSheet("color: white; font-size: 18px;")
        sim_layout.addWidget(self.clock_label)

        # Horizontal Layout for on/off button and sim speed combo box
        simOptions_layout = QHBoxLayout()

        # Create a QComboBox for simulation speed
        self.speed_combo_box = QComboBox()
        self.speed_combo_box.setStyleSheet("color: white; background-color: #772CE8;")
        self.speed_combo_box.addItems(["1x", "10x", "50x"])  # Example speed options
        self.speed_combo_box.currentTextChanged.connect(self.simSpeedSelected)
        simOptions_layout.addWidget(self.speed_combo_box)

        # Create on/off button for the simulation
        operational_button = QPushButton("Start")
        operational_button.setStyleSheet("background-color: green; color: black;")
        operational_button.clicked.connect(self.operationalClicked)
        simOptions_layout.addWidget(operational_button)

        # Add the horizontal layout containing the combo box and on/off button to sim_layout
        sim_layout.addLayout(simOptions_layout)

        # Add the vertical layout containing the clock and sim options to speed_layout
        speed_layout.addLayout(sim_layout)

        # Set the layout for the speed frame
        speed_frame.setLayout(speed_layout)
        grid_layout.addWidget(speed_frame, 0, 1)



        # 3. Schedule Builder Section (Middle)
        schedule_frame = self.create_section_frame(800, 250)  # Reduced height
        schedule_layout = QVBoxLayout()
        schedule_label = QLabel("Schedule Builder")
        schedule_label.setStyleSheet("color: white; font-size: 18px;")
        schedule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        schedule_layout.addWidget(schedule_label)

        # Add widgets for schedule builder (placeholders)
        schedule_layout.addWidget(QLabel("Auto/Manual Toggle goes here", alignment=Qt.AlignmentFlag.AlignCenter))
        schedule_frame.setLayout(schedule_layout)
        grid_layout.addWidget(schedule_frame, 1, 0, 1, 2)  # Span two columns

        # 4. Dispatch Rate Section (Lower left)
        dispatch_frame = self.create_section_frame(400, 150)
        dispatch_layout = QVBoxLayout()
        dispatch_label = QLabel("Dispatch Rate")
        dispatch_label.setStyleSheet("color: white; font-size: 18px;")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        dispatch_layout.addWidget(dispatch_label)

        # Add widgets for dispatch rate (placeholders)
        dispatch_layout.addWidget(QLabel("4 Trains/hr display goes here", alignment=Qt.AlignmentFlag.AlignCenter))
        dispatch_frame.setLayout(dispatch_layout)
        grid_layout.addWidget(dispatch_frame, 2, 0)

        # 5. Train Data Section (Lower right)
        train_frame = self.create_section_frame(400, 150)
        train_layout = QVBoxLayout()
        train_label = QLabel("Train Data")
        train_label.setStyleSheet("color: white; font-size: 18px;")
        train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_layout.addWidget(train_label)

        # Add widgets for train data (placeholders)
        train_layout.addWidget(QLabel("Train data display goes here", alignment=Qt.AlignmentFlag.AlignCenter))
        train_frame.setLayout(train_layout)
        grid_layout.addWidget(train_frame, 2, 1)

        # 6. Block Occupancies (Bottom, spanning both columns)
        blocks_frame = self.create_section_frame(800, 275)
        blocks_layout = QVBoxLayout()

        # Upper portion of Block Occupancies
        upper_blocks_label = QLabel("Block Occupancies")
        upper_blocks_label.setStyleSheet("color: white; font-size: 18px;")
        upper_blocks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        blocks_layout.addWidget(upper_blocks_label)

        # Spacer to take up remaining space and push the lower part down
        blocks_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Lower portion of Block Occupancies
        blocks_layout.addWidget(QLabel("Block occupancies go here", alignment=Qt.AlignmentFlag.AlignCenter))  # Placeholder for the lower section
        blocks_frame.setLayout(blocks_layout)
        grid_layout.addWidget(blocks_frame, 3, 0, 1, 2)  # Span two columns

        layout.addLayout(grid_layout)

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

    # Custom dialog for user to select maintenance closure line
    def closureClicked(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Maintenance Report")

        # Apply styles to the dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: #171717;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #772ce8;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #772ce8;
                color: #ffffff;
                selection-background-color: #CCCCFF;
                selection-color: #000000;
            }
            QLineEdit {
                background-color: #772ce8;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #ffffff;
            }
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Create label
        label = QLabel("What Block Requries Maintenance?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create combo box with options
        combo_box = QComboBox()
        combo_box.addItems(["Blue"])
        h_layout.addWidget(combo_box)

        # Create text entry box
        text_entry = QLineEdit()
        text_entry.setPlaceholderText("1 - 15")
        h_layout.addWidget(text_entry)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_closure(dialog, combo_box.currentText(), text_entry.text()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_closure(self, dialog, line, block):
        block = int(block)
        self.maintenance_blocks.append((line, block))
        self.maintenance_blocks = sorted(self.maintenance_blocks, key=lambda x: x[1])
        self.occupied_blocks.append((line, block))
        self.occupied = sorted(self.occupied_blocks, key=lambda x: x[1])
        self.open_blocks.remove((line, block))
        print(self.maintenance_blocks)
        print(self.occupied_blocks)
        print(self.open_blocks)
        print("Block", block, "on the", line, "line has been closed for maintenance!")
        dialog.accept()

    # The functionality for user opening a block from maintenance
    def openingClicked(self):
        print('in openingClicked')
        dialog = QDialog(self)
        dialog.setWindowTitle("Maintenance Report")

        # Apply styles to the dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: #171717;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #772ce8;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #772ce8;
                color: #ffffff;
                selection-background-color: #CCCCFF;
                selection-color: #000000;
            }
            QLineEdit {
                background-color: #772ce8;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #ffffff;
            }
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Create label
        label = QLabel("What Block Needs Opened?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create combo box with options
        combo_box = QComboBox()
        combo_box.addItems(["Blue"])
        h_layout.addWidget(combo_box)

        # Create text entry box
        text_entry = QLineEdit()
        text_entry.setPlaceholderText("1 - 15")
        h_layout.addWidget(text_entry)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_opening(dialog, combo_box.currentText(), text_entry.text()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_opening(self, dialog, line, block):
        print('in submit_opening')
        block = int(block)
        self.open_blocks.append((line, block))
        self.open_blocks = sorted(self.open_blocks, key=lambda x: x[1])
        self.maintenance_blocks.remove((line, block))
        self.occupied_blocks.remove((line, block))
        print(self.maintenance_blocks)
        print(self.maintenance_blocks)
        print(self.open_blocks)

        print("Block", block, "on the", line, "line has been reopened from maintenance!")
        dialog.accept()  

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()

    sys.exit(app.exec())
