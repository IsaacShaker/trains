import sys
import time
import pandas as pd
from train import Train
from TrackController import TrackController
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QInputDialog, QDialog, QLineEdit, QFileDialog, QScrollArea, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QTimer

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.simulationRunning = False #this is necessary for clock to work properly

        self.oldTime = 21600 # the system will began at 6AM
        self.speed = 1 # the system will be running at 1x speed by default

        # Helps with toggling mode button text
        self.automatic_mode = True # the system begins in automatic mode

        # Create the open block list, everything should open upon creation
        self.open_blocks = []
        for i in range(1,17): # fill the list with all necesary blocks
            self.open_blocks.append(('Blue',i))

        # Create the maintenance blocks list
        self.maintenance_blocks = []

        # Create the occupied block list
        self.occupied_blocks = []

        # Create the occupied blocks list that includes maintenance
        self.nates_occupied_blocks = []

        # Create the trains list
        self.trains = []

        # Create a Track Controller
        self.wayside = TrackController()

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

        # Helps with toggling crossing button text
        self.crossing_status = True

        # Helps with toggling switch button text
        self.switch_status = True

        # Helps with toggling top light text
        self.top_light_status = True

        # Helps with toggling bottom light text
        self.bottom_light_status = True

    # Create the Home and Test Bench tab for the window
    def create_tabs(self):
        # Home Tab content
        home = QWidget()
        home_layout = QVBoxLayout()

        # Call the layout with frames to organize the UI for Home tab
        self.create_home_layout(home_layout)
        home.setLayout(home_layout)
        home.setStyleSheet("background-color: #171717;")  # Black background

        # Test Bench content
        test_bench = QWidget()
        test_bench_layout = QVBoxLayout()

        # Call the layout with frames to organize the UI for Test Bench tab
        self.create_test_bench_layout(test_bench_layout)
        test_bench.setLayout(test_bench_layout)
        test_bench.setStyleSheet("background-color: #171717;")  # Black background        

        # Add the tabs to the tab widget
        self.tab_widget.addTab(home, "Home")
        self.tab_widget.addTab(test_bench, "Test Bench")

    # Create the layout for all the Test Bench widgets
    def create_test_bench_layout(self, layout):
        # Main grid layout for Test Bench tab
        grid_layout = QGridLayout()

        # Set the layout margins and spacing
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed
        grid_layout.setSpacing(10)  # Adjust spacing between widgets

        # Create the widget for Wayside Controller label
        wayside_frame = self.create_section_frame(250, 200)
        wayside_layout = QVBoxLayout()
        
        # Add the label to the frame
        wayside_label = QLabel("Block Occupancies")
        wayside_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        wayside_label.setStyleSheet("color: white; font-size: 20px;")
        wayside_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        wayside_layout.addWidget(wayside_label)

        # Create the QListWidget for the wayside occupancies checklist
        self.wayside_occupancies = QListWidget()
        self.wayside_occupancies.setStyleSheet("""
            QListWidget::item {
                padding: 1px;  /* Add padding to increase item size */
                font-size: 20px;  /* Increase font size to make items larger */
            }
        """)

        # Create the wayside blocks list
        self.wayside_blocks = [f'Blue {i}' for i in range(1, 17)]  # Create block labels dynamically

        # Add the wayside blocks as options for the checklist
        for block in self.wayside_blocks:
            block_option = QListWidgetItem(block)
            block_option.setFlags(block_option.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            block_option.setCheckState(Qt.CheckState.Unchecked)  # Initial status is unchecked
            self.wayside_occupancies.addItem(block_option)

        # Add submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.submit_button.setStyleSheet("background-color: green; color: white;")
        self.submit_button.clicked.connect(self.submit_test_bench)

        # Add the QListWidget to the layout
        wayside_layout.addWidget(self.wayside_occupancies)

        wayside_layout.addWidget(self.submit_button)

        # Set the final layout for the frame and add it to the grid layout
        wayside_frame.setLayout(wayside_layout)
        grid_layout.addWidget(wayside_frame, 0, 0, 1, 2)

        # Layout for buttons
        signals_frame = self.create_section_frame(250, 200)

        # Layout for bottom half
        signals_big_layout = QVBoxLayout()

        # Label for Signals
        signals_label = QLabel('Traffic Signals')
        signals_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        signals_label.setStyleSheet("color: white; font-size: 20px;")
        signals_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        signals_big_layout.addWidget(signals_label)

        # Layout for the interactives
        signals_small_layout = QHBoxLayout()

        # Button for railway crossing
        self.crossing_button = QPushButton("Railway Crossing")
        self.crossing_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.crossing_button.setStyleSheet("background-color: green; color: white; font-size: 20px;")
        self.crossing_button.clicked.connect(self.crossing_clicked)
        signals_small_layout.addWidget(self.crossing_button)

        # Button for switch
        self.switch_button = QPushButton("5-->6")
        self.switch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.switch_button.setStyleSheet("background-color: blue; color: white; font-size: 20px;")
        self.switch_button.clicked.connect(self.switch_clicked)
        signals_small_layout.addWidget(self.switch_button)

        # Light on Blue #6
        self.top_light = QPushButton("Top Track Light")
        self.top_light.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.top_light.setStyleSheet("background-color: green; color: white; font-size: 20px;")
        self.top_light.clicked.connect(self.top_light_clicked)
        signals_small_layout.addWidget(self.top_light)        

        # Light on Blue #11
        self.bottom_light = QPushButton("Bottom Track Light")
        self.bottom_light.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.bottom_light.setStyleSheet("background-color: green; color: white; font-size: 20px")
        self.bottom_light.clicked.connect(self.bottom_light_clicked)
        signals_small_layout.addWidget(self.bottom_light)

        signals_big_layout.addLayout(signals_small_layout)
        signals_frame.setLayout(signals_big_layout)
        grid_layout.addWidget(signals_frame, 1, 0, 1, 2)
        
        # Add the grid layout to the main layout provided as a parameter
        layout.addLayout(grid_layout)

    # Handle what happend when the crossing is changed
    def crossing_clicked(self):
        self.crossing_status = not(self.crossing_status)
        if self.crossing_status == False:
            self.crossing_button.setStyleSheet("background-color: red; color: white; font-size: 20px")
        else:
            self.crossing_button.setStyleSheet("background-color: green; color: white; font-size: 20px")

    # Handle what happens when the switch is changed
    def switch_clicked(self):
        self.switch_status = not(self.switch_status)

        if self.switch_status == False:
            self.switch_button.setText('5-->12')
            self.switch_button.setStyleSheet("background-color: blue; color: white; font-size: 20px")
        else:
            self.switch_button.setText('5-->6')
            self.switch_button.setStyleSheet("background-color: blue; color: white; font-size: 20px")

    # Handle what happens when the top light changes states
    def top_light_clicked(self):
        self.top_light_status = not(self.top_light_status)
        if self.top_light_status == False:
            self.top_light.setText('Top Track Light')
            self.top_light.setStyleSheet("background-color: red; color: white; font-size: 20px")
        else:
            self.top_light.setText('Top Track Light')
            self.top_light.setStyleSheet("background-color: green; color: white; font-size: 20px")

    # Handle what happens when the bottom light changes states
    def bottom_light_clicked(self):
        self.bottom_light_status = not(self.bottom_light_status)
        if self.bottom_light_status == False:
            self.bottom_light.setText('Bottom Track Light')
            self.bottom_light.setStyleSheet("background-color: red; color: white; font-size: 20px")
        else:
            self.bottom_light.setText('Bottom Track Light')
            self.bottom_light.setStyleSheet("background-color: green; color: white; font-size: 20px")

    # Handle the user confirming their Test Bench selection for occupancies
    def submit_test_bench(self):
        for i in range(self.wayside_occupancies.count()):
            block = self.wayside_occupancies.item(i)
            block_text = block.text()
            block_number = int(block_text.split()[1])
            new_block = ('Blue', block_number)
            if block.checkState() == Qt.CheckState.Checked:
                if self.occupied_blocks.count(new_block) == 0:
                    self.occupied_blocks.append(new_block)
                    self.open_blocks.remove(new_block)
            if block.checkState() == Qt.CheckState.Unchecked:
                if self.open_blocks.count(new_block) == 0:
                    self.open_blocks.append(new_block)
                    self.occupied_blocks.remove(new_block)

    # Create the layout for all the Home widgets
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
        self.rate_label = QLabel("Trains/hr")
        self.rate_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        dispatch_layout.addWidget(self.rate_label)
        dispatch_frame.setLayout(dispatch_layout)
        grid_layout.addWidget(dispatch_frame, 2, 0)

        # 5. Train Data Section (Lower right)
        train_frame = self.create_section_frame(250, 200)
        train_layout = QVBoxLayout()
        self.train_date_label = QLabel("Train Data")
        self.train_date_label.setStyleSheet("color: white; font-size: 20px;")
        self.train_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_layout.addWidget(self.train_date_label)

        # Create Hbox for Train Data widgets
        self.train_data_big_layout = QHBoxLayout()

        # Create Vbox for authority and suggested speed
        self.train_data_small_layout = QVBoxLayout()

        # Create the label for train authority
        self.train_authority_label = QLabel("Authority")
        self.train_authority_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.train_authority_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        self.train_authority_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_small_layout.addWidget(self.train_authority_label)

        #Create the label for suggested speed
        self.train_suggested_speed_label = QLabel("Suggested Speed")
        self.train_suggested_speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.train_suggested_speed_label.setStyleSheet("background-color: blue; color: white; font-size: 16px;")
        self.train_suggested_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_small_layout.addWidget(self.train_suggested_speed_label)
        self.train_data_big_layout.addLayout(self.train_data_small_layout)

        # Create the label for train selection
        self.train_label = QLabel("Train")
        self.train_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.train_label.setStyleSheet("background-color: #772ce8; color: white; font-size: 16px;")
        self.train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_big_layout.addWidget(self.train_label)

        train_layout.addLayout(self.train_data_big_layout)
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

        # Blocks for making our labels
        blocks = [('Blue', i+1) for i in range(16)]

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

    # Function for making all frames for widgets consistent
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
        self.nates_occupied_blocks.append((line, block))
        self.nates_occupied_blocks = sorted(self.nates_occupied_blocks, key=lambda x: x[1])
        self.open_blocks.remove((line, block))
        new_block = (line, block)

        # Change background color accordingly
        if new_block in self.block_labels:
            block_label = self.block_labels[new_block]
            self.update_label_background(block_label, new_block)

        print("Block", block, "on the", line, "line has been closed for maintenance!")
        print("Sending proper signals to prevent trains from entering block Blue #"+str(block)+"...")
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
        self.nates_occupied_blocks.remove(block)
        self.update_opening_button_state()

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

    # Format the time to the form of a clock
    def format_time(self, seconds: int) -> str:
        hours = (seconds // 3600) % 24
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Update the clock every realtime second that passes
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

            for block in self.open_blocks:
                block_label = self.block_labels[block]
                self.update_label_background(block_label, block)

            for block in self.maintenance_blocks:
                block_label = self.block_labels[block]
                self.update_label_background(block_label, block)

            for block in self.occupied_blocks:
                block_label = self.block_labels[block]
                self.update_label_background(block_label, block)

            print('-------------Switch Safety-------------')
            # Perform possible safety meaures relating to the switch
            for train in self.trains:
                if train.destination == "STATION: B" and self.switch_status == False and self.occupied_blocks.count(('Blue', 4)):
                    print('Wrong Switch scenario')
                    # Prevent train for going the wrong way
                    train.setSuggestedSpeed(0)
                    self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
                elif train.destination == "STATION: C" and self.switch_status == True and self.occupied_blocks.count(('Blue', 4)):
                    print('Wrong Switch Scenario')
                    # Prevent train for going the wrong way
                    train.setSuggestedSpeed(0)
                    self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
                elif train.destination == "STATION: B" and self.top_light_status == False and self.occupied_blocks.count(('Blue', 6)):
                    print('Top Light Scenario')
                    # Prevent train from running the light
                    train.setSuggestedSpeed(0)
                    self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
                elif train.destination == "STATION: C" and self.bottom_light_status == False and self.occupied_blocks.count(('Blue', 12)):
                    print('Bottom Light Measure')
                    # Prevent train from running the light
                    train.setSuggestedSpeed(0)
                    self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
                elif self.crossing_status == False and self.occupied_blocks.count(('Blue', 3)):
                    print('Railway Crossing Measure')
                    # Prevent train from running the railway crossing
                    train.setSuggestedSpeed(0)
                    self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
                else:
                    print('Good')
                    # Keep Suggested Speed the same
                    if train.suggested_speed == 0:
                        train.setSuggestedSpeed(50)
                        self.train_suggested_speed_label.setText('Suggested Speed = 31 mph')
                print('---------------------------------')

    # What happens when the user presses Current Mode button
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

    # Open file explorer on the user's device
    def upload_clicked(self):
        print('Uploading a schedule...')
        
        # Open file explorer on the user's device
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Microsoft Excel Worksheet (*.xlsx);")
        if file_path:
            print('Now running', file_path)
            
            try:
                # Read the Excel file
                df = pd.read_excel(file_path, na_filter=False)
            
            except Exception as e:
                print(f"Error reading the Excel file: {e}")
        else:
            print("No file selected.")

        # Access row 0, column 1 using .iloc
        new_line = df.iloc[0,0]
        new_destination = df.iloc[0, 1]
        new_time = df.iloc[0, 2]
        train_count = len(self.trains)
        if train_count == 0:
            new_train = 'Train0'
        else:
            new_train = 'Train'+str(train_count)

        print(new_train, 'on the', new_line, 'line will arrive at', new_destination, 'in', new_time, 'minutes!')
        rate_string = str(len(self.trains) + 1)+' Trains/hr'
        self.rate_label.setText(rate_string)
        new_train = Train(new_train, new_line, new_destination, new_time)
        if new_train.destination == 'STATION: B':
            new_train.setAuthority(550)
            new_train.setSuggestedSpeed(50)
        elif new_train.destination == 'STATION: C':
            new_train.setAuthority(500)
            new_train.setSuggestedSpeed(50)
        else:
            print('Station does not exist')

        if len(self.trains) == 0: # If we are adding the first train, delete the label
            # Remove the current QLabel
            self.train_data_big_layout.removeWidget(self.train_label)
            self.train_label.deleteLater()  # Delete QLabel
        else:
            # Remove the QComboBox
            self.train_data_big_layout.removeWidget(self.train_data_combo_box)
            self.train_data_combo_box.deleteLater() # Delete QComboBox

        self.trains.append(new_train)

        # Create the QComboBox
        self.train_data_combo_box = QComboBox()
        self.train_data_combo_box.setPlaceholderText('Train')
        self.train_data_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.train_data_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
        for train in self.trains:
            self.train_data_combo_box.addItem(train.name)
        self.train_data_combo_box.currentTextChanged.connect(self.train_selected)

        # Add the QComboBox to the layout
        self.train_data_big_layout.addWidget(self.train_data_combo_box)

    # Allow the user to select the destination and time of a train
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

    # Create the train object
    def submit_dispatch(self, dialog, station, time):
        Train0 = Train('Train0', 'Blue', station, time)
        rate_string = str(len(self.trains) + 1)+' Trains/hr'
        self.rate_label.setText(rate_string)
        print('Dispatching',Train0.name, 'on the', Train0.line, 'line, to', Train0.destination, 'at', Train0.arrival_time)
        dialog.accept()

    # Display the correct data based on the train selected
    def train_selected(self, selected_train):
        print('You selected', selected_train)
        for train in self.trains:
            if train.name == selected_train:
                my_train = train
            else:
                pass

        print('Displaying info on', selected_train,':')
        print('Authority =', my_train.authority, 'm')
        print('Suggested Speed =', my_train.suggested_speed, 'kph')
        imperial_authority = my_train.authority * 3.28084 # Convert from metric
        imperial_authority = round(imperial_authority)
        auth_str = 'Authority = '+str(imperial_authority)+' ft'
        self.train_authority_label.setText(auth_str)
        imperial_suggested_speed = my_train.suggested_speed * 0.621371 # Convert from metric
        imperial_suggested_speed = round(imperial_suggested_speed)
        speed_str = 'Suggested Speed = '+str(imperial_suggested_speed)+' mph'
        self.train_suggested_speed_label.setText(speed_str)

    # Function to update label background based on block status
    def update_label_background(self, label, block):
        if block in self.maintenance_blocks:
            #print('Yellow')
            label.setStyleSheet("background-color: yellow; color: black;")
        elif block in self.open_blocks:
            #print('Green')
            label.setStyleSheet("background-color: green; color: white;")
        elif block in self.occupied_blocks:
            #print('Red')
            label.setStyleSheet("background-color: red; color: white;")
        else:
            label.setStyleSheet("background-color: gray; color: white;")  # Default color
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()

    sys.exit(app.exec())