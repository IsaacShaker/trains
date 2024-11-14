import sys
import time
import pandas as pd
import requests
from train import Train
from clock import Clock
from scheduleReader import ScheduleReader
from station import Station
from block import Block
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QInputDialog, QDialog, QLineEdit, QFileDialog, QScrollArea, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from collections import defaultdict, deque

# Create an object from Clock class
myClock = Clock()

URL = 'http://127.0.0.1:5000'

class MyWindow(QMainWindow, Clock, Train, Station, Block):
    def __init__(self):
        super().__init__()

        self.oldTime = 21600 # the system will began at 6AM
        self.speed = 1 # the system will be running at 1x speed by default

        # Helps with toggling mode button text
        self.automatic_mode = True # the system begins in automatic mode

        # Create the maintenance blocks set
        self.maintenance_blocks = set()

        # Create the occupied block set
        self.occupied_blocks = set()

        # Create the recently opened block set
        self.recently_opened = set()

        # Create a set for recent speed_hazards
        self.recent_speed_hazards = set()

        # Create the trains list
        self.trains = []

        # Create the stations and add them to a list
        self.green_stations = []
        self.yard = Station("STATION; YARD", [0])
        self.green_stations.append(self.yard)
        self.glenbury = Station("STATION; GLENBURY", [65,114])
        self.green_stations.append(self.glenbury)
        self.dormont = Station("STATION; DORMONT", [73,105])
        self.green_stations.append(self.dormont)
        self.mt_lebanon = Station("STATION; MT LEBANON", [77])
        self.green_stations.append(self.mt_lebanon)
        self.poplar = Station("STATION; POPLAR", [88])
        self.green_stations.append(self.poplar)
        self.castle_shannon = Station("STATION; CASTLE SHANNON", [96])
        self.green_stations.append(self.castle_shannon)
        self.overbrook = Station("STATION; OVERBROOK", [123, 57])
        self.green_stations.append(self.overbrook)
        self.inglewood = Station("STATION; INGLEWOOD", [132, 48])
        self.green_stations.append(self.inglewood)
        self.central = Station("STATION; CENTRAL", [141, 39])
        self.green_stations.append(self.central)
        self.whited = Station("STATION; WHITED", [22])
        self.green_stations.append(self.whited)
        self.edgebrook = Station("STATION; EDGEBROOK", [9])
        self.green_stations.append(self.edgebrook)
        self.pioneer = Station("STATION; PIONEER", [2])
        self.green_stations.append(self.pioneer)
        self.south_bank = Station("STATION; SOUTH BANK", [31])
        self.green_stations.append(self.south_bank)


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
        self.timer.timeout.connect(self.second_passed)

        # Initialize the start timeand total elapsed time
        self.start_time = time.time()
        self.timer.start(1000)  # Update every second

        ##################################################
        #     Create the blocks from the Track Layout    #
        ##################################################
        file_path = 'C:/Trains C/trains/CTC/Blocks.xlsx'
        self.blocks = defaultdict(list)
        for line_color in ['Green', 'Red']:
            excel_sheet = line_color+" Line"
            blocks_df = pd.read_excel(file_path, sheet_name=excel_sheet)            
            
            # Loop through each row and create a Block instance
            for _, row in blocks_df.iterrows():
                block_number = row['Block Number']
                speed_limit = row['Speed Limit (Km/Hr)']
                
                # Create a new Block instance and store it in the nested dictionary
                new_block = Block(line_color, block_number, speed_limit)
                self.blocks[line_color].append(new_block)

        ###################################################
        #               Integration Stuff                 #
        ###################################################
        self.block_for_wayside = 0
        self.status_for_wayside = False
        self.line_for_wayside = ""
        self.authority_for_wayside = 0
        self.speed_for_wayside = 0
        
        #                   Dictionaries                  #
        # Maintenance Blocks
        self.maintenance_blocks_dict = {
            "line": self.line_for_wayside,
            "index": self.block_for_wayside,
            "maintenance": self.status_for_wayside
        }

        # Authority
        self.authority_dict = {
            "line": self.line_for_wayside,
            "index": self.block_for_wayside,
            "authority": self.authority_for_wayside
        }

        # Suggested Speed
        self.suggested_speed_dict = {
            "line": self.line_for_wayside,
            "index": self.block_for_wayside,
            "speed": self.speed_for_wayside
        }

        self.index
        self.output_block
        # Wayside Vision
        self.wayside_vision_dict = {
            "index" : self.index,
            "output_block": self.output_block
        }

        #               Timer Stuff                 #
        # self.request_block_occupancies_timer = QTimer(self)
        # self.request_block_occupancies_timer.timeout.connect(self.receive_block_occupancies)
        # self.request_block_occupancies_timer.start(1000)

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
        self.wayside_blocks = [f'Green {i}' for i in range(1, 17)]  # Create block labels dynamically

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
        for i in range(self.wayside_occupancies.len()):
            block = self.wayside_occupancies.item(i)
            block_text = block.text()
            block_number = int(block_text.split()[1])
            new_block = ('Green', block_number)
            if block.checkState() == Qt.CheckState.Checked:
                if new_block in self.maintenance_blocks:
                    print("Train cannot move to block Green #"+str(block_number)+" since it is under maintenance")
                elif new_block not in self.occupied_blocks and new_block not in self.maintenance_blocks:
                    self.occupied_blocks.append(new_block)
            if block.checkState() == Qt.CheckState.Unchecked:
                    self.occupied_blocks.remove(new_block)

    # Create the layout for all the Home widgets
    def create_home_layout(self, layout):
        # Main layout grid for Home tab
        grid_layout = QGridLayout()

        # Set the layout margins and spacing
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed
        grid_layout.setSpacing(10)  # Adjust spacing between widgets

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
        closure_button.clicked.connect(self.closure_clicked)
        button_layout.addWidget(closure_button)  # Add the Closure button to the horizontal layout

        # Define Maintenance Opening button as an instance attribute
        self.opening_button = QPushButton("Opening")
        self.opening_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self.clock_label = QLabel(myClock.format_time(0))
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
        self.speed_combo_box.currentTextChanged.connect(self.sim_speed_selected)
        simOptions_layout.addWidget(self.speed_combo_box)

        # Create on/off button for the simulation
        operational_button = QPushButton("Start")
        operational_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        operational_button.setStyleSheet("background-color: green; color: white;")
        operational_button.clicked.connect(self.operational_clicked)
        simOptions_layout.addWidget(operational_button)

        # Add the horizontal layout containing the combo box and on/off button to sim_layout
        sim_layout.addLayout(simOptions_layout)

        # Add the vertical layout containing the clock and sim options to speed_layout
        speed_layout.addLayout(sim_layout)

        # Set the layout for the speed frame
        speed_frame.setLayout(speed_layout)
        grid_layout.addWidget(speed_frame, 0, 1)



        # 3. Schedule Builder Section (Middle)
        schedule_frame = self.create_section_frame(650, 325)  # Reduced height
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

        # Add Hbox for upload/dispatch buttons
        self.upload_dispatch_layout = QHBoxLayout()

        # Add the upload button
        self.upload_button = QPushButton('Upload a Schedule')
        self.upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.upload_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
        self.upload_button.clicked.connect(self.upload_clicked)
        self.upload_dispatch_layout.addWidget(self.upload_button)

        # Add a Vbox Layout for all of the sub buttons for dispatching
        self.dispatch_options_layout = QVBoxLayout()

        # Add the label for Green Line
        self.green_line_label = QLabel('Green Line')
        self.green_line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.green_line_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        self.green_line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.dispatch_options_layout.addWidget(self.green_line_label)

        # Add the label for train selection when in auto mode
        self.schedule_train_label = QLabel('Select Train')
        self.schedule_train_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.schedule_train_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        self.schedule_train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.dispatch_options_layout.addWidget(self.schedule_train_label)

        # Add Hbox for for station selection and time enterance
        self.station_and_time_layout = QHBoxLayout()

        # Add the label for station selection when in auto mode
        self.station_select_label = QLabel('Select Station')
        self.station_select_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.station_select_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        self.station_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.station_and_time_layout.addWidget(self.station_select_label)

        # Add the label for time entrance when in auto mode
        self.time_select_label = QLabel('Arrival Time')
        self.time_select_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.time_select_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
        self.time_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.station_and_time_layout.addWidget(self.time_select_label)

        # Add station and time sections to layout
        self.dispatch_options_layout.addLayout(self.station_and_time_layout)

        # Add a confirm button for dispatching a train
        self.confirm_dispatch_button = QPushButton("Confirm")
        self.confirm_dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.confirm_dispatch_button.setStyleSheet("background-color: gray; color: white; font-size: 18px;")
        self.dispatch_options_layout.addWidget(self.confirm_dispatch_button)

        self.upload_dispatch_layout.addLayout(self.dispatch_options_layout)

        # Add upload/dispatch button to QHBoxLayout
        mode_layout.addLayout(self.upload_dispatch_layout)

        # Add the QHBoxLayout to the main schedule layout
        schedule_layout.addLayout(mode_layout)

        # Set Layout for frame
        schedule_frame.setLayout(schedule_layout)
        grid_layout.addWidget(schedule_frame, 1, 0, 1, 2)



        # 4. Dispatch Rate Section (Lower left)
        dispatch_frame = self.create_section_frame(200, 125)
        dispatch_layout = QVBoxLayout()
        dispatch_label = QLabel("Dispatch Rate")
        dispatch_label.setStyleSheet("color: white; font-size: 20px;")
        dispatch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        dispatch_layout.addWidget(dispatch_label)

        # Add widgets for dispatch rate (placeholders)
        self.rate_label = QLabel("Trains/hr")
        self.rate_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.rate_label.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        self.rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        dispatch_layout.addWidget(self.rate_label)
        dispatch_frame.setLayout(dispatch_layout)
        grid_layout.addWidget(dispatch_frame, 2, 0)



        # 5. Train Data Section (Lower right)
        train_frame = self.create_section_frame(375, 125)
        train_layout = QVBoxLayout()
        self.train_data_label = QLabel("Train Data")
        self.train_data_label.setStyleSheet("color: white; font-size: 20px;")
        self.train_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        train_layout.addWidget(self.train_data_label)

        # Create Hbox for Train Data widgets
        self.train_data_big_layout = QHBoxLayout()

        # Create Vbox for authority and suggested speed
        self.train_data_small_layout = QVBoxLayout()

        # Create the label for train authority
        self.train_authority_label = QLabel("Authority")
        self.train_authority_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.train_authority_label.setStyleSheet("background-color: green; color: white; font-size: 14px;")
        self.train_authority_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_small_layout.addWidget(self.train_authority_label)

        #Create the label for suggested speed
        self.train_suggested_speed_label = QLabel("Suggested Speed")
        self.train_suggested_speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.train_suggested_speed_label.setStyleSheet("background-color: green; color: white; font-size: 12px;")
        self.train_suggested_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_small_layout.addWidget(self.train_suggested_speed_label)
        self.train_data_big_layout.addLayout(self.train_data_small_layout)

        # Create the label for train selection
        self.train_label = QLabel("Train")
        self.train_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.train_label.setStyleSheet("background-color: #772ce8; color: white; font-size: 12px;")
        self.train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_big_layout.addWidget(self.train_label)

        train_layout.addLayout(self.train_data_big_layout)
        train_frame.setLayout(train_layout)
        grid_layout.addWidget(train_frame, 2, 1)



        # 6. Block Occupancies (Bottom)
        blocks_frame = self.create_section_frame(650, 225)
        blocks_layout = QVBoxLayout()

        # Label for Block Occupancies
        block_occupancies_label = QLabel("Block Occupancies")
        block_occupancies_label.setStyleSheet("color: white; font-size: 20px;")
        block_occupancies_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        blocks_layout.addWidget(block_occupancies_label)

        # Create grid for the blocks
        self.blocks_grid_layout = QGridLayout()

        number = 1
        # Create 10x15 grid
        for row in range(10):
            for col in range(15):
                block_label = QLabel(str(number))  # Convert number to string for QLabel text
                block_label.setStyleSheet("background-color: green; color: white; font-size: 10px;")
                block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                self.blocks_grid_layout.addWidget(block_label, row, col)
                self.block_labels['Green', number] = block_label
                number += 1

        blocks_layout.addLayout(self.blocks_grid_layout)
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
    def closure_clicked(self):
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

        # Create Cbox for Line
        line_combo_box = QComboBox()
        line_combo_box.addItems(["Green", "Red"])
        h_layout.addWidget(line_combo_box)

        # Create Cbox for Block
        block_combo_box = QComboBox()
        maintenance_numbers = {block[1] for block in self.maintenance_blocks}
        for i in range(1, 151):
            if i not in maintenance_numbers:
                block_combo_box.addItems([str(i)])
        h_layout.addWidget(block_combo_box)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_closure(dialog, line_combo_box.currentText(), block_combo_box.currentText()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_closure(self, dialog, line, block):
        block = int(block)
        new_block = (line, block)
        if new_block in self.occupied_blocks:
            print('Cannot place block under maintenance since train is occupying block')
        else:
            self.maintenance_blocks.add((line, block))
            print(self.maintenance_blocks)
            self.update_opening_button_state()

            # Change background color accordingly
            #if new_block in self.block_labels:
            block_label = self.block_labels[new_block]
            self.update_label_background()

            # Send maintenance block to wayside
            self.maintenance_blocks_dict["line"] = line
            self.maintenance_blocks_dict["index"] = block
            self.maintenance_blocks_dict["maintenance"] = True
            while(1):
                print('closure')
                response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
                if response.status_code == 200:
                    break

            print("Block", block, "on the", line, "line has been closed for maintenance!")
            dialog.accept()

    # The functionality for user opening a block from maintenance
    def opening_clicked(self):
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
            line_combo_box.addItem(f"{block[0]} #{block[1]}")
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
        block_line, block_number_str = open_block.split(" #")
        block_number = int(block_number_str)
        block = (block_line, block_number)
        self.recently_opened.add(block)
        self.maintenance_blocks.remove(block)
        print(self.maintenance_blocks)
        self.update_opening_button_state()

        # Change background color accordingly
        self.update_label_background()

        # Send maintenance block to wayside
        self.maintenance_blocks_dict["line"] = block_line
        self.maintenance_blocks_dict["index"] = block_number
        self.maintenance_blocks_dict["maintenance"] = False
        while(1):
            print('opening')
            response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
            if response.status_code == 200:
                break

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
            self.opening_button.clicked.connect(self.opening_clicked)  # Enable click functionality
        else:
            self.opening_button.setEnabled(False)  # Disable the button
            self.opening_button.setStyleSheet("background-color: gray; color: white;")

    # The functionality of the user selecting the Simulation Speed of the system
    def sim_speed_selected(self, speed):
        print("The simulation is now running at", speed, "speed!")
        myClock.sim_speed = int(speed[:-1])  # Extracting the numeric value from the selected string

    # The functionality of the user starting the simulation
    def operational_clicked(self):
        # Toggle the simulation state
        if not myClock.simulation_running:
            myClock.simulation_running = True
            myClock.elapsed_time = time.time()  # Reset start time when simulation starts
            print("The simulation has started!")
        else:
            myClock.simulation_running = False
            print("The simulation has been stopped!")

        # Update the button text to reflect the current state
        sender = self.sender()  # Get the button that triggered the event
        if myClock.simulation_running:
            sender.setText("Stop")  # Change the button text to "Stop" when running
            sender.setStyleSheet("background-color: red; color: white;")
        else:
            sender.setText("Start")  # Change the button text back to "Start" when stopped
            sender.setStyleSheet("background-color: green; color: white;")

    # Update the clock every realtime second that passes
    def second_passed(self):
        # Only update the clock if the simulation is running
        if myClock.simulation_running:
            # Update the clock for everybody 
            myClock.update_clock()

            # Update the label in UI
            self.clock_label.setText(myClock.current_time)

            for block in self.maintenance_blocks:
                block_label = self.block_labels[block]
                self.update_label_background(block_label, block)

            for block in self.occupied_blocks:
                block_label = self.block_labels[block]
                self.update_label_background(block_label, block)

            # print('-------------Switch Safety-------------')
            # # Perform possible safety meaures relating to the switch
            # for train in self.trains:
            #     if train.destination == "STATION: B" and self.switch_status == False and self.occupied_blocks.count(('Green', 4)):
            #         print('Wrong Switch scenario')
            #         # Prevent train for going the wrong way
            #         train.setSuggestedSpeed(0)
            #         self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
            #     elif train.destination == "STATION: C" and self.switch_status == True and self.occupied_blocks.count(('Green', 4)):
            #         print('Wrong Switch Scenario')
            #         # Prevent train for going the wrong way
            #         train.setSuggestedSpeed(0)
            #         self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
            #     elif train.destination == "STATION: B" and self.top_light_status == False and self.occupied_blocks.count(('Green', 6)):
            #         print('Top Light Scenario')
            #         # Prevent train from running the light
            #         train.setSuggestedSpeed(0)
            #         self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
            #     elif train.destination == "STATION: C" and self.bottom_light_status == False and self.occupied_blocks.count(('Green', 12)):
            #         print('Bottom Light Measure')
            #         # Prevent train from running the light
            #         train.setSuggestedSpeed(0)
            #         self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
            #     elif self.crossing_status == False and self.occupied_blocks.count(('Blue', 3)):
            #         print('Railway Crossing Measure')
            #         # Prevent train from running the railway crossing
            #         train.setSuggestedSpeed(0)
            #         self.train_suggested_speed_label.setText('Suggested Speed = 0 mph')
            #     else:
            #         print('Good')
            #         # Keep Suggested Speed the same
            #         if train.suggested_speed == 0:
            #             train.setSuggestedSpeed(50)
            #             self.train_suggested_speed_label.setText('Suggested Speed = 31 mph')
            #     print('---------------------------------')

    # What happens when the user presses Current Mode button
    def mode_clicked(self):        
        # Toggle the mode first
        self.automatic_mode = not self.automatic_mode

        if self.automatic_mode:
            # Switch to Automatic Mode
            self.mode_button.setText('Current Mode: Automatic Mode')
            self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")

        else:
            # Switch to Manual Mode
            self.mode_button.setText('Current Mode: Manual Mode')
            self.mode_button.setStyleSheet("background-color: green; color: white; font-size: 18px")

        # Update the button states based on the new mode
        self.update_mode_button_state()

    # Method to update the Mode button's state dynamically
    def update_mode_button_state(self):
        # No need to disconnect any signals, just update the state
        if self.automatic_mode:
            # Enable upload button
            self.upload_button.setEnabled(True)
            self.upload_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 18px")
            
            # Delete all previous widgets to turn them into labels
            self.dispatch_options_layout.removeWidget(self.green_line_label)
            self.green_line_label.deleteLater()
            self.dispatch_options_layout.removeWidget(self.schedule_train_combo_box)
            self.schedule_train_combo_box.deleteLater()
            self.station_and_time_layout.removeWidget(self.station_select_combo_box)
            self.station_select_combo_box.deleteLater()
            self.station_and_time_layout.removeWidget(self.time_select_edit)
            self.time_select_edit.deleteLater()
            self.dispatch_options_layout.removeWidget(self.confirm_dispatch_button)
            self.confirm_dispatch_button.deleteLater()
            self.dispatch_options_layout.deleteLater()
            self.station_and_time_layout.deleteLater()

            # Add a Vbox Layout for all of the sub buttons for dispatching
            self.dispatch_options_layout = QVBoxLayout()

            # Add the label for Green Line
            self.green_line_label = QLabel('Green Line')
            self.green_line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_line_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
            self.green_line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.dispatch_options_layout.addWidget(self.green_line_label)

            # Add the label for train selection when in auto mode
            self.schedule_train_label = QLabel('Select Train')
            self.schedule_train_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.schedule_train_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
            self.schedule_train_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.dispatch_options_layout.addWidget(self.schedule_train_label)

            # Add Hbox for station selection and time enterance
            self.station_and_time_layout = QHBoxLayout()

            # Add the label for station selection when in auto mode
            self.station_select_label = QLabel('Select Station')
            self.station_select_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.station_select_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
            self.station_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.station_and_time_layout.addWidget(self.station_select_label)

            # Add the label for time entrance when in auto mode
            self.time_select_label = QLabel('Arrival Time')
            self.time_select_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.time_select_label.setStyleSheet("background-color: gray; color: white; font-size: 18px")
            self.time_select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.station_and_time_layout.addWidget(self.time_select_label)

            # Add station and time sections to layout
            self.dispatch_options_layout.addLayout(self.station_and_time_layout)

            # Add a confirm button for dispatching a train
            self.confirm_dispatch_button = QPushButton("Confirm")
            self.confirm_dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.confirm_dispatch_button.setStyleSheet("background-color: gray; color: white; font-size: 18px;")
            self.dispatch_options_layout.addWidget(self.confirm_dispatch_button)

            self.upload_dispatch_layout.addLayout(self.dispatch_options_layout)

        else:
            # Disable upload button
            self.upload_button.setEnabled(False)
            self.upload_button.setStyleSheet("background-color: gray; color: white; font-size: 18px")

            # Delete all previous labels to turn them into widgets
            self.dispatch_options_layout.removeWidget(self.green_line_label)
            self.green_line_label.deleteLater()
            self.dispatch_options_layout.removeWidget(self.schedule_train_label)
            self.schedule_train_label.deleteLater()
            self.station_and_time_layout.removeWidget(self.station_select_label)
            self.station_select_label.deleteLater()
            self.station_and_time_layout.removeWidget(self.time_select_label)
            self.time_select_label.deleteLater()
            self.dispatch_options_layout.removeWidget(self.confirm_dispatch_button)
            self.confirm_dispatch_button.deleteLater()
            self.dispatch_options_layout.deleteLater()
            self.station_and_time_layout.deleteLater()

            # Add a Vbox Layout for all of the sub buttons for dispatching
            self.dispatch_options_layout = QVBoxLayout()

            # Add the label for Green Line
            self.green_line_label = QLabel('Green Line')
            self.green_line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_line_label.setStyleSheet("background-color: green; color: white; font-size: 18px")
            self.green_line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.dispatch_options_layout.addWidget(self.green_line_label)

            # Add combo box for train select
            self.schedule_train_combo_box = QComboBox()
            self.schedule_train_combo_box.setPlaceholderText('Select Train')
            self.schedule_train_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.schedule_train_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.schedule_train_combo_box.addItem('New Train')
            for train in self.trains:
                self.schedule_train_combo_box.addItem(train.name)
            self.dispatch_options_layout.addWidget(self.schedule_train_combo_box)

            # Add Hbox for for station selection and time enterance
            self.station_and_time_layout = QHBoxLayout()

            # Add combo box for station selection
            self.station_select_combo_box = QComboBox()
            self.station_select_combo_box.setPlaceholderText('Select Station')
            self.station_select_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.station_select_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.station_select_combo_box.addItems(["GLENBURY", "DORMONT", "MT LEBANON", "POPLAR", "CASTLE SHANNON","OVERBROOK", "INGLEWOOD", "CENTRAL", "WHITED", "EDGEBROOK", "PIONEER", "LEBRON", "SOUTH BANK"])
            self.station_and_time_layout.addWidget(self.station_select_combo_box)

            # Add time entrance
            self.time_select_edit = QLineEdit()
            time_regex = QRegularExpression(r"^(2[0-3]|[01]\d):([0-5]\d):([0-5]\d)$")
            validator = QRegularExpressionValidator(time_regex)
            self.time_select_edit.setValidator(validator)
            self.time_select_edit.setPlaceholderText("Arrival Time")
            self.station_and_time_layout.addWidget(self.time_select_edit)

            # Add station and time sections to layout
            self.dispatch_options_layout.addLayout(self.station_and_time_layout)

            # Enable Confirm button
            self.confirm_dispatch_button = QPushButton("Confirm")
            self.confirm_dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.confirm_dispatch_button.setStyleSheet("background-color: green; color: white; font-size: 18px;")
            self.confirm_dispatch_button.clicked.connect(self.submit_dispatch)
            self.dispatch_options_layout.addWidget(self.confirm_dispatch_button)

            self.upload_dispatch_layout.addLayout(self.dispatch_options_layout)

    # Open file explorer on the user's device
    def upload_clicked(self):        
        # Open file explorer on the user's device
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Microsoft Excel Worksheet (*.xlsx);")
        if file_path:
            pass            
            try:
                # Read the Excel file
                new_trains = myScheduleReader.get_green_routes(file_path)
                for i in new_trains:
                    self.trains.append(i)
            
            except Exception as e:
                print(f"Error reading the Excel file: {e}")
        else:
            print("No file selected.")

        self.train_data_big_layout.removeWidget(self.train_label)
        self.train_label.deleteLater()

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

    # Create the train object
    def submit_dispatch(self):
        print('------------------------------------------------------')
        selected_name = self.schedule_train_combo_box.currentText()
        if selected_name == 'New Train': # Create a new train
            if len(self.trains) == 0:
                new_train = 'Train 1'
            else:
                new_train = 'Train '+str(len(self.trains) + 1)

            new_train = Train(new_train, 'Green')
            print(new_train.name, 'on the Green line will arrive at', self.station_select_combo_box.currentText() ,'at', self.time_select_edit.text())
            rate_string = str(len(self.trains) + 1) +' Trains/hr'
            self.rate_label.setText(rate_string)
            self.schedule_train_combo_box.addItem(new_train.name)
            
            new_train.add_stop(self.station_select_combo_box.currentText())
            new_train.get_authority_from_map()

            # Set time to release train from yard
            time = self.time_select_edit.text()
            # Split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, time.split(":"))
            time_in_seconds = hours * 3600 + minutes * 60 + seconds
            hours = time_in_seconds // 3600
            minutes = (time_in_seconds % 3600) //60
            seconds = time_in_seconds % 60
            print('arrival time =', hours, minutes, seconds)
            new_train.set_first_arrival_time(time_in_seconds)
            hours = new_train.dispatch_time // 3600
            minutes = (new_train.dispatch_time % 3600) //60
            seconds = new_train.dispatch_time % 60
            print('dispatch time =', hours, minutes, seconds)

            # Convert authorities to tuples for a list
            auth_list = []
            for authority in new_train.route_authorities:
                auth_list.append([new_train.name, authority])
            
            # Populate the stations
            self.yard.add_authority(auth_list[0])
            new_train.route_authorities.popleft()

            for stop in new_train.station_stops:
                for station in self.green_stations:
                    if station.name == stop:
                        station.add_authority(auth_list[0])
                    elif station.name in ('STATION; POPLAR', 'STATION; CASTLE SHANNON', 'STATION; EDGEBROOK', 'STATION; PIONEER', 'STATION; SOUTH BANK'):
                        station.add_authority([new_train.name, -1])
                    elif station.name == 'STATION; YARD':
                        pass
                    else:
                        station.add_authority([new_train.name, -1])
                        station.add_authority([new_train.name, -1])

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

        else: # Add a stop to the train
            selected_train = next((train for train in self.trains if train.name == selected_name), None)
            #selected_train.route_authorities.clear()
            selected_train.add_stop(self.station_select_combo_box.currentText())
            selected_train.get_authority_from_map()
            

    # Display the correct data based on the train selected
    def train_selected(self, selected_train):
        for train in self.trains:
            if train.name == selected_train:
                my_train = train
            else:
                pass

        print('Displaying info on', selected_train,':')
        print('Authority =', my_train.get_authority(), 'm')
        print('Suggested Speed =', my_train.get_suggested_speed(), 'kph')
        imperial_authority = my_train.get_authority() * 3.28084 # Convert from metric
        imperial_authority = round(imperial_authority)
        auth_str = 'Authority = '+str(imperial_authority)+' ft'
        self.train_authority_label.setText(auth_str)
        imperial_suggested_speed = my_train.get_suggested_speed() * 0.621371 # Convert from metric
        imperial_suggested_speed = round(imperial_suggested_speed)
        speed_str = 'Suggested Speed = '+str(imperial_suggested_speed)+' mph'
        self.train_suggested_speed_label.setText(speed_str)

    # Function to update label background based on block status
    def update_label_background(self):
        for block in self.maintenance_blocks:
            block_label = self.block_labels[block[0], block[1]]
            block_label.setStyleSheet("background-color: yellow; color: black;")
            block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        for block in self.occupied_blocks:
            block_label = self.block_labels[block[0], block[1]]
            block_label.setStyleSheet("background-color: red; color: white;")
            block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for block in self.recently_opened:
            block_label = self.block_labels[block[0], block[1]]
            block_label.setStyleSheet("background-color: green; color: white;")
            block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.recently_opened.clear()
        
    # Function for receicing block occupancies from wayside
    def receive_block_occupancies(self):
        response = requests.get(URL + "/track-controller-sw/get-data/block_data")

        data_dict = {}

        if response.status_code == 200:
            data_dict = response.json()
        else:
            print("Failed to retrieve data", response.text)
            return
        
        self.occupied_blocks.clear()
        # Update my block occupancies based on received block occupancies
        for block in data_dict["Green"]:
            new_block = ("Green", block["block"])
            if new_block in self.maintenance_blocks:
                continue
            else:
                if (block["occupied"] == True):
                    self.occupied_blocks.add(new_block)
                    
                else:
                    self.recently_opened.add(new_block)

        for station in self.green_stations:
            station_id = station.get_location()
            for id in station_id:
                if ('Green', id) in self.occupied_blocks and station.get_popped() == False:
                    # Send authority to wayside since just entered station block
                    self.authority_dict["line"] = "Green"
                    self.authority_dict["index"] = id
                    popped_auth = station.pop_authority()
                    self.authority_dict["authority"] = popped_auth[1]
                    for train in self.trains:
                        if train.name == popped_auth[0]:
                            train.set_current_authority(popped_auth[1])
                            if len(train.station_stops):
                                self.wayside_vision_dict["index"] = 1
                                self.wayside_vision_dict["output_block"] = 0
                                while(1):
                                    response = requests.post(URL + "/track-controller-sw/give-data/wayside-vsion", json=self.wayside_vision_dict)
                                    if response.status_code == 200:
                                        break
                            else:
                                self.wayside_vision_dict["index"] = 1
                                self.wayside_vision_dict["output_block"] = 58
                                while(1):
                                    response = requests.post(URL + "/track-controller-sw/give-data/wayside-vsion", json=self.wayside_vision_dict)
                                    if response.status_code == 200:
                                        break
                    station.set_popped(True)
                    # Send Wayside Vision
                    self.wayside_vision_dict["index"] = 2
                    self.wayside_vision_dict["output_block"] = 0
                    while(1):
                        response = requests.post(URL + "/track-controller-sw/give-data/authority", json=self.authority_dict)
                        if response.status_code == 200:
                            break

        for station in self.green_stations:
            station_id = station.get_location()
            if ('Green', station_id) in self.recently_opened:
                station.set_popped(False)
                self.wayside_vision_dict["index"] = 2
                self.wayside_vision_dict["output_block"] = 62
                while(1):
                    response = requests.post(URL + "/track-controller-sw/give-data/wayside-vsion", json=self.wayside_vision_dict)
                    if response.status_code == 200:
                        break


        # Speed Stuff 
        for block in data_dict["Green"]:
            if block["speed_hazard"] == True and ("Green", block["block"]) not in self.recent_speed_hazards: # Add to speed hazard set
                # Change speed to zero
                self.recent_speed_hazards.add(("Green", block["block"]))
                self.suggested_speed_dict["line"] = "Green"
                self.suggested_speed_dict["index"] = block["block"]
                self.suggested_speed_dict["speed"] = 0
                for train in self.trains:
                    train.set_suggested_speed(0)
                while(1):
                    response = requests.post(URL + "/track-controller-sw/give-data/speed", json=self.suggested_speed_dict)
                    if response.status_code == 200:
                        break
            elif block["speed_hazard"] == False and ("Green", block["block"]) in self.recent_speed_hazards:
                # Change speed to actual
                self.recent_speed_hazards.remove(("Green", block["block"]))
                self.suggested_speed_dict["line"] = "Green"
                self.suggested_speed_dict["index"] = block["block"]
                blk = self.blocks["Green"][block["block"]]
                self.suggested_speed_dict["speed"] = blk.get_block_speed()
                for train in self.trains:
                    train.set_suggested_speed(blk.get_block_speed())
                while(1):
                    response = requests.post(URL + "/track-controller-sw/give-data/speed", json=self.suggested_speed_dict)
                    if response.status_code == 200:
                        break

        self.update_label_background()

        # Wayside Vision stuff


    # Update the wayside vision dictionary
    def update_wayside_vision(self):
        pass
        

    # API function for wayside vision
    def get_wayside_vision(self):
        return self.wayside_vision_dict

if __name__ == "__main__":    
    app = QApplication(sys.argv)

    # Create an object from the ScheduleReader class
    myScheduleReader = ScheduleReader()

    window = MyWindow()
    window.show()

    sys.exit(app.exec())