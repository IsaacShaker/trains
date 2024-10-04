import sys
import time
from train import Train
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QInputDialog, QDialog, QLineEdit, QFileDialog, QScrollArea
from PyQt6.QtCore import Qt, QTimer

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulationRunning = False #this is necessary for clock to work properly

        self.oldTime = 21600 # the system will began at 6AM
        self.speed = 1 # the system will be running at 1x speed by default

        self.automatic_mode = True # the system begins in automatic mode

        # Create the open block list, everything should open upon creation
        self.open_blocks = []
        for i in range(1,17): # fill the list with all necesary blocks
            self.open_blocks.append(('Blue',i))

        # Create the maintenance blocks list
        self.maintenance_blocks = []

        # Create the occupied block list
        self.occupied_blocks = []

        # Create the trains list
        trains = []

        # Dictionary for block labels in block occupancy tab
        self.block_labels = {}

        # Set the window title
        self.setWindowTitle("CTC Office")

        # Set a fixed size for the window
        self.setFixedSize(700, 875)  # Width: 850, Height: 875

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
        test_bench_label.setStyleSheet("color: white; font-size: 20px;")
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

        # Define Maintenance Opening button as an instance attribute
        self.opening_button = QPushButton("Opening")

        # 1. Initial setup for Maintenance Section (Top left)
        maintenance_frame = self.create_section_frame(250, 80)
        maintenance_layout = QHBoxLayout()
        maintenance_label = QLabel("Maintenance")
        maintenance_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        maintenance_label.setStyleSheet("color: white; font-size: 20px;")
        maintenance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        maintenance_layout.addWidget(maintenance_label)

        # Vertical layout for Closure and Opening buttons
        button_layout = QVBoxLayout()

        # Define Maintenance Closure button
        closure_button = QPushButton("Closure")
        closure_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        closure_button.setStyleSheet("background-color: yellow; color: black;")
        closure_button.clicked.connect(self.closureClicked)
        button_layout.addWidget(closure_button)  # Add the Closure button to the horizontal layout

        self.opening_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Add the Opening button to the layout
        button_layout.addWidget(self.opening_button)

        # Add the vertical button layout to the maintenance frame layout
        maintenance_layout.addLayout(button_layout)
        maintenance_frame.setLayout(maintenance_layout)
        grid_layout.addWidget(maintenance_frame, 0, 0)

        # Update the button's state initially based on maintenance_blocks
        self.update_opening_button_state()


        # 2. Simulation Speed Section (Top right)
        speed_frame = self.create_section_frame(250, 80)  # Reduced height
        speed_layout = QHBoxLayout()  # Using QHBoxLayout to align items horizontally
        speed_label = QLabel("Simulation Speed")
        speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        speed_label.setStyleSheet("color: white; font-size: 20px;")
        speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        speed_layout.addWidget(speed_label)

        # Vertical layout for Clock and Simulation Speed
        sim_layout = QVBoxLayout()

        # Add the clock label
        self.clock_label = QLabel(self.format_time(0))
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
        self.speed_combo_box.addItems(["1x", "10x", "50x"])  # Example speed options
        self.speed_combo_box.currentTextChanged.connect(self.simSpeedSelected)
        simOptions_layout.addWidget(self.speed_combo_box)

        # Create on/off button for the simulation
        operational_button = QPushButton("Start")
        operational_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        operational_button.setStyleSheet("background-color: green; color: white;")
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
        schedule_frame = self.create_section_frame(650, 200)  # Reduced height
        schedule_layout = QVBoxLayout()
        schedule_label = QLabel("Schedule Builder")
        schedule_label.setStyleSheet("color: white; font-size: 20px;")
        schedule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        schedule_layout.addWidget(schedule_label)

        # Add Hbox for Mode switch and upload/dispatch buttons
        mode_layout = QVBoxLayout()

        # Add the Mode button
        self.mode_button = QPushButton('Current Mode: Automatic Mode')
        self.mode_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
        self.mode_button.clicked.connect(self.mode_clicked)
        mode_layout.addWidget(self.mode_button)

        #Add Vbox for upload/dispatch buttons
        upload_dispatch_layout = QHBoxLayout()

        # Add the upload button
        self.upload_button = QPushButton('Upload a Schedule')
        self.upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.upload_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
        self.upload_button.clicked.connect(self.upload_clicked)
        upload_dispatch_layout.addWidget(self.upload_button)

        # Add the dispatch button (we want this disabled since starting in auto mode)
        self.dispatch_button = QPushButton('Dispatch a Train')
        self.dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dispatch_button.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        self.dispatch_button.clicked.connect(self.dispatch_clicked)
        self.dispatch_button.setEnabled(False)
        upload_dispatch_layout.addWidget(self.dispatch_button)

        # Add upload/dispatch button to QHBoxLayout
        mode_layout.addLayout(upload_dispatch_layout)

        # Add the QHBoxLayout to the main schedule layout
        schedule_layout.addLayout(mode_layout)

        # Set Layout for frame
        schedule_frame.setLayout(schedule_layout)
        grid_layout.addWidget(schedule_frame, 1, 0, 1, 2)

        # 4. Dispatch Rate Section (Lower left)
        dispatch_frame = self.create_section_frame(250, 200)
        dispatch_layout = QVBoxLayout()
        dispatch_label = QLabel("Dispatch Rate")
        dispatch_label.setStyleSheet("color: white; font-size: 20px;")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        dispatch_layout.addWidget(dispatch_label)

        # Add widgets for dispatch rate (placeholders)
        rate_label = QLabel("x Trains/hr")
        rate_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        dispatch_layout.addWidget(rate_label)
        dispatch_frame.setLayout(dispatch_layout)
        grid_layout.addWidget(dispatch_frame, 2, 0)

        # 5. Train Data Section (Lower right)
        train_frame = self.create_section_frame(250, 200)
        train_layout = QVBoxLayout()
        train_label = QLabel("Train Data")
        train_label.setStyleSheet("color: white; font-size: 20px;")
        train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_layout.addWidget(train_label)

        # Create Hbox for Train Data widgets
        train_data_big_layout = QHBoxLayout()

        # Create Vbox for authority and suggested speed
        train_data_small_layout = QVBoxLayout()

        # Create the combo box to select a train
        self.train_data_combo_box = QComboBox()
        self.train_data_combo_box.setPlaceholderText('Train')
        self.train_data_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.train_data_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
        self.train_data_combo_box.addItems(["Train 0", "Train 1"])  # Example speed options
        self.train_data_combo_box.currentTextChanged.connect(self.train_selected)
        train_data_big_layout.addWidget(self.train_data_combo_box)

        # Create the label for train authority
        train_authority_label = QLabel("Authority = x m")
        train_authority_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        train_authority_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        train_authority_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_data_small_layout.addWidget(train_authority_label)

        #Create the label for suggested speed
        train_suggested_speed_label = QLabel("Suggested Speed = v mph")
        train_suggested_speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        train_suggested_speed_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        train_suggested_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_data_small_layout.addWidget(train_suggested_speed_label)

        train_data_big_layout.addLayout(train_data_small_layout)
        train_layout.addLayout(train_data_big_layout)
        train_frame.setLayout(train_layout)
        grid_layout.addWidget(train_frame, 2, 1)

        # 6. Block Occupancies (Bottom)
        blocks_frame = self.create_section_frame(650, 275)
        blocks_layout = QVBoxLayout()

        # Upper portion of Block Occupancies
        upper_blocks_label = QLabel("Block Occupancies")
        upper_blocks_label.setStyleSheet("color: white; font-size: 20px;")
        upper_blocks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        blocks_layout.addWidget(upper_blocks_label)

        # Lower portion of Block Occupancies
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #ffffff;        /* Background color of the scrollbar */
                width: 15px;
                margin: 15px 3px 15px 3px;
            }

            QScrollBar::handle:vertical {
                background: #772ec8;        /* Handle (thumb) color */
                min-height: 20px;
            }

            QScrollBar::add-line:vertical {
                background: #333;
                height: 15px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                background: #333;
                height: 15px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: 2px solid grey;
                width: 3px;
                height: 3px;
                background: white;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # Create a widget to hold all the lines of data
        data_widget = QWidget()
        data_layout = QVBoxLayout()

        # Create a widget to hold all the lines of data
        data_widget = QWidget()
        data_layout = QVBoxLayout()

        # Example of 15 blocks
        blocks = [('Blue', i+1) for i in range(15)]  # Block names are ('Blue', 1), ('Blue', 2), ..., ('Blue', 15)

        # Add 15 lines of data as QLabel widgets and update their background color
        for block in blocks:
            block_label = QLabel(f"Block #{block[1]}")
            self.block_labels[block] = block_label #store the label in the dictionary
            block_label.setMinimumHeight(30)
            block_label.setMinimumWidth(600)
            # Pass the label and the block to the function to update the background color
            self.update_label_background(block_label, block)
            data_layout.addWidget(block_label)


        data_widget.setLayout(data_layout)
        scroll_area.setWidget(data_widget)

        # Add the scroll area to the main layout
        blocks_layout.addWidget(scroll_area)
        blocks_frame.setLayout(blocks_layout)
        grid_layout.addWidget(blocks_frame, 3, 0, 1, 2)

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
        text_entry.setPlaceholderText("1 - 16")
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
        self.update_opening_button_state()
        self.occupied_blocks.append((line, block))
        self.occupied = sorted(self.occupied_blocks, key=lambda x: x[1])
        self.open_blocks.remove((line, block))
        new_block = (line, block)

        # Change background color accordingly
        if new_block in self.block_labels:
            block_label = self.block_labels[new_block]
            self.update_label_background(block_label, new_block)

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
        h_layout = QVBoxLayout()

        # Create combo box with options
        line_combo_box = QComboBox()
        for block in self.maintenance_blocks:
            line_combo_box.addItem(f"{block[0]} - Block #{block[1]}")
        h_layout.addWidget(line_combo_box)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_opening(dialog, line_combo_box.currentText()))
        h_layout.addWidget(button)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_opening(self, dialog, open_block):
        block_line, block_number_str = open_block.split(" - ")
        block_number_str = block_number_str[7:]
        block_number = int(block_number_str)
        block = (block_line, block_number)
        self.open_blocks.append(block)
        self.open_blocks = sorted(self.open_blocks, key=lambda x: x[1])
        self.maintenance_blocks.remove(block)
        self.update_opening_button_state()
        self.occupied_blocks.remove(block)

        # Change background color accordingly
        if block in self.block_labels:
            block_label = self.block_labels[block]
            self.update_label_background(block_label, block)

        print("Block", block_line, "on the", block_number, "line has been reopened from maintenance!")
        dialog.accept()  

    # Method to update the Opening button's state dynamically
    def update_opening_button_state(self):
        try:
            # Try disconnecting the clicked signal if it's already connected
            self.opening_button.clicked.disconnect()
        except TypeError:
            # If there's nothing to disconnect, just pass
            pass

        # Update the button's state based on whether there are maintenance blocks
        if len(self.maintenance_blocks) > 0:
            self.opening_button.setEnabled(True)
            self.opening_button.setStyleSheet("background-color: green; color: black;")
            self.opening_button.clicked.connect(self.openingClicked)  # Enable click functionality
        else:
            self.opening_button.setEnabled(False)  # Disable the button
            self.opening_button.setStyleSheet("background-color: gray; color: white;")

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

    def mode_clicked(self):        
        # Toggle the mode first
        self.automatic_mode = not self.automatic_mode

        if self.automatic_mode:
            # Switch to Automatic Mode
            print('Switched to Automatic Mode')
            self.mode_button.setText('Current Mode: Automatic Mode')
            self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
        else:
            # Switch to Manual Mode
            print('Switched to Manual Mode')
            self.mode_button.setText('Current Mode: Manual Mode')
            self.mode_button.setStyleSheet("background-color: green; color: white; font-size: 18px")

        # Update the button states based on the new mode
        self.update_mode_button_state()

    # Method to update the Mode button's state dynamically
    def update_mode_button_state(self):
        # No need to disconnect any signals, just update the state
        if self.automatic_mode:
            # Automatic Mode: Enable Upload, Disable Dispatch
            self.upload_button.setEnabled(True)
            self.upload_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
            
            self.dispatch_button.setEnabled(False)
            self.dispatch_button.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        else:
            # Manual Mode: Enable Dispatch, Disable Upload
            self.dispatch_button.setEnabled(True)
            self.dispatch_button.setStyleSheet("background-color: green; color: white; font-size: 18px")
            
            self.upload_button.setEnabled(False)
            self.upload_button.setStyleSheet("background-color: gray; color: white; font-size: 18px")

    def upload_clicked(self):
        print('Uploading a schedule...')

        # Open file explorer on the user's device
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;Text Files (*.txt)")
        if file_name:
            print('Now running', file_name)

    def dispatch_clicked(self):
        print('Dispatching a train...')
        dialog = QDialog(self)
        dialog.setWindowTitle("Train Dispatcher")

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
        label = QLabel("Where and when would you like to dispatch a train?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create combo box with options
        combo_box = QComboBox()
        combo_box.addItems(["Station B", "Station C"])
        h_layout.addWidget(combo_box)

        # Create text entry box
        text_entry = QLineEdit()
        text_entry.setPlaceholderText("HH:MM:SS")
        h_layout.addWidget(text_entry)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_dispatch(dialog, combo_box.currentText(), text_entry.text()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    def submit_dispatch(self, dialog, station, time):
        Train0 = Train('Train0', 'Blue', station, time)
        print('Dispatching',Train0.name, 'on the', Train0.line, 'line, to', Train0.destination, 'at', Train0.arrival_time)
        dialog.accept()

    def train_selected(self):
        print('You selected a train')

    # Function to update label background based on block status
    def update_label_background(self, label, block):
        if block in self.maintenance_blocks:
            label.setStyleSheet("background-color: yellow; color: black;")
        elif block in self.open_blocks:
            label.setStyleSheet("background-color: green; color: white;")
        elif block in self.occupied_blocks:
            label.setStyleSheet("background-color: red; color: white;")
        else:
            label.setStyleSheet("background-color: gray; color: white;")  # Default color
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()

    sys.exit(app.exec())