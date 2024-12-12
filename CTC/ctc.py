import os
import sys
import time
import pandas as pd
import requests
from CTC.train import Train
#from CTC.clock import Clock
from CTC.scheduleReader import ScheduleReader
from CTC.station import Station
from CTC.block import Block
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QComboBox, QInputDialog, QDialog, QLineEdit, QFileDialog, QScrollArea, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QTimer, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from collections import defaultdict

base_path = os.path.dirname(os.path.abspath(__file__))  # Full path of the current file's directory
# Set the file_path to one directory up from base_path and join it with 'block.csv'
FILE_PATH = os.path.join(base_path, '..', 'CTC', 'Blocks.xlsx')
# Normalize the path to remove any redundant separators
FILE_PATH = os.path.abspath(FILE_PATH)

# Create an object from Clock class
#myClock = Clock()

myScheduleReader = ScheduleReader()

URL = 'http://127.0.0.1:5000'

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #myClock.old_time = 21600 # the system will began at 6AM
        #myClock.sim_speed = 1 # the system will be running at 1x speed by default
        self.current_time = "00:00:00"
        self.enable_clock = False
        self.seconds_cum = 0
        self.sim_speed = 1

        self.system_time = 0

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

        # Create the green stations and add them to a list
        self.green_stations = []
        self.green_yard = Station("STATION; YARD", [0])
        self.green_stations.append(self.green_yard)
        self.glenbury_out = Station("STATION; GLENBURY OUT", [65])
        self.green_stations.append(self.glenbury_out)
        self.glenbury_in = Station("STATION; GLENBURY IN", [114])
        self.green_stations.append(self.glenbury_in)
        self.dormont_out = Station("STATION; DORMONT OUT", [73])
        self.green_stations.append(self.dormont_out)
        self.dormont_in = Station("STATION; DORMONT IN", [105])
        self.green_stations.append(self.dormont_in)
        self.mt_lebanon = Station("STATION; MT LEBANON", [77])
        self.green_stations.append(self.mt_lebanon)
        self.poplar = Station("STATION; POPLAR", [88])
        self.green_stations.append(self.poplar)
        self.castle_shannon = Station("STATION; CASTLE SHANNON", [96])
        self.green_stations.append(self.castle_shannon)
        self.overbrook_out = Station("STATION; OVERBROOK OUT", [123])
        self.green_stations.append(self.overbrook_out)
        self.overbrook_in = Station("STATION; OVERBROOK IN", [57])
        self.green_stations.append(self.overbrook_in)
        self.inglewood_out = Station("STATION; INGLEWOOD OUT", [132])
        self.green_stations.append(self.inglewood_out)
        self.inglewood_in = Station("STATION; INGLEWOOD IN", [48])
        self.green_stations.append(self.inglewood_in)
        self.central_out = Station("STATION; CENTRAL OUT", [141])
        self.green_stations.append(self.central_out)
        self.central_in = Station("STATION; CENTRAL IN", [39])
        self.green_stations.append(self.central_in)
        self.whited = Station("STATION; WHITED", [22])
        self.green_stations.append(self.whited)
        self.lebron = Station("STATION; LEBRON", [16])
        self.green_stations.append(self.lebron)
        self.edgebrook = Station("STATION; EDGEBROOK", [9])
        self.green_stations.append(self.edgebrook)
        self.pioneer = Station("STATION; PIONEER", [2])
        self.green_stations.append(self.pioneer)
        self.south_bank = Station("STATION; SOUTH BANK", [31])
        self.green_stations.append(self.south_bank)

        # Create the red stations and add them to a list
        self.red_stations = []
        self.red_yard = Station("STATION; YARD", [0])
        self.red_stations.append(self.red_yard)
        self.shadyside = Station("STATION; SHADYSIDE", [7])
        self.red_stations.append(self.shadyside)
        self.herron_ave = Station("STATION; HERRON AVE", [16])
        self.red_stations.append(self.herron_ave)
        self.swissville = Station("STATION; SWISSVILLE", [21])
        self.red_stations.append(self.swissville)
        self.penn_station = Station("STATION; PENN STATION", [25])
        self.red_stations.append(self.penn_station)
        self.steel_plaza = Station("STATION; STEEL PLAZA", [35])
        self.red_stations.append(self.steel_plaza)
        self.first_ave = Station("STATION; FIRST AVE", [45])
        self.red_stations.append(self.first_ave)
        self.station_sqaure = Station("STATION; STATION SQUARE", [48])
        self.red_stations.append(self.station_sqaure)
        self.south_hills_junction = Station("STATION; SOUTH HILLS JUNCTION", [60])
        self.red_stations.append(self.south_hills_junction)


        # Bool for helping switch the occupancies grid
        self.viewing_green = True

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
        # self.timer.timeout.connect(self.second_passed)

        # Initialize the start timeand total elapsed time
        self.start_time = time.time()
        self.timer.start(1000)  # Update every second

        ##################################################
        #     Create the blocks from the Track Layout    #
        ##################################################
        self.blocks = defaultdict(list)
        for line_color in ['Green', 'Red']:
            excel_sheet = line_color+" Line"
            blocks_df = pd.read_excel(FILE_PATH, sheet_name=excel_sheet)            
            
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
        self.yard_was_occupied = False
        
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

        self.index = 0 
        self.output_block = 0
        # Wayside Vision
        self.wayside_vision_dict = {
            "line": self.line_for_wayside,
            "index" : self.index,
            "output_block": self.output_block
        }

        self.sim_speed_dict = {
            "sim_speed": self.sim_speed
        }

        self.clock_enable_dict = {
            "enable": self.enable_clock
        }

        self.line = ""
        self.train_initializer_dict = {
            "line": self.line,
            "id": self.index
        }

        self.clock_enable_dict_dict = {
            "enable": self.enable_clock
        }

        #               Timer Stuff                 #
        self.request_block_occupancies_timer = QTimer(self)
        self.request_block_occupancies_timer.timeout.connect(self.receive_block_occupancies)
        self.request_block_occupancies_timer.start(1000)

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

        # Add layout for occupancies
        occupancies_layout = QHBoxLayout()

        # Create the QListWidget for the wayside occupancies checklist
        self.green_wayside_occupancies = QListWidget()
        self.green_wayside_occupancies.setStyleSheet("""
            QListWidget::item {
                padding: 1px;  /* Add padding to increase item size */
                font-size: 20px;  /* Increase font size to make items larger */
            }
        """)
        self.red_wayside_occupancies = QListWidget()
        self.red_wayside_occupancies.setStyleSheet("""
            QListWidget::item {
                padding: 1px;  /* Add padding to increase item size */
                font-size: 20px;  /* Increase font size to make items larger */
            }
        """)

        # Create the wayside blocks list
        self.green_wayside_blocks = [f'Green {i}' for i in range(1, 151)]
        self.red_wayside_blocks  = [f'Red {i}' for i in range(1,76)]

        # Add the wayside blocks as options for the checklist
        for block in self.green_wayside_blocks:
            block_option = QListWidgetItem(block)
            block_option.setFlags(block_option.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            block_option.setCheckState(Qt.CheckState.Unchecked)  # Initial status is unchecked
            self.green_wayside_occupancies.addItem(block_option)
        occupancies_layout.addWidget(self.green_wayside_occupancies)

        for block in self.red_wayside_blocks:
            block_option = QListWidgetItem(block)
            block_option.setFlags(block_option.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            block_option.setCheckState(Qt.CheckState.Unchecked)  # Initial status is unchecked
            self.red_wayside_occupancies.addItem(block_option)
        occupancies_layout.addWidget(self.red_wayside_occupancies)

        # Add submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.submit_button.setStyleSheet("background-color: green; color: white;")
        self.submit_button.clicked.connect(self.submit_test_bench)

        # Add the QListWidget to the layout
        wayside_layout.addLayout(occupancies_layout)
        wayside_layout.addWidget(self.submit_button)
        # Set the final layout for the frame and add it to the grid layout
        wayside_frame.setLayout(wayside_layout)
        grid_layout.addWidget(wayside_frame, 0, 0, 1, 2)
        
        # Add the grid layout to the main layout provided as a parameter
        layout.addLayout(grid_layout)

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

        # Vertical layout for Closure and Opening buttons
        green_button_layout = QVBoxLayout()

        # Define Maintenance Closure button
        green_closure_button = QPushButton("Closure")
        green_closure_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        green_closure_button.setStyleSheet("background-color: green; color: white;")
        green_closure_button.clicked.connect(self.green_closure_clicked)
        green_button_layout.addWidget(green_closure_button)  # Add the Closure button to the horizontal layout

        # Define Maintenance Opening button as an instance attribute
        self.green_opening_button = QPushButton("Opening")
        self.green_opening_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        green_button_layout.addWidget(self.green_opening_button)
        maintenance_layout.addLayout(green_button_layout)

        maintenance_label = QLabel("Maintenance")
        maintenance_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        maintenance_label.setStyleSheet("color: white; font-size: 20px;")
        maintenance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label
        maintenance_layout.addWidget(maintenance_label)

        # Vertical layout for Closure and Opening buttons
        red_button_layout = QVBoxLayout()

        # Define Maintenance Closure button
        red_closure_button = QPushButton("Closure")
        red_closure_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        red_closure_button.setStyleSheet("background-color: red; color: white;")
        red_closure_button.clicked.connect(self.red_closure_clicked)
        red_button_layout.addWidget(red_closure_button)  # Add the Closure button to the horizontal layout

        # Define Maintenance Opening button as an instance attribute
        self.red_opening_button = QPushButton("Opening")
        self.red_opening_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        red_button_layout.addWidget(self.red_opening_button)
        maintenance_layout.addLayout(red_button_layout)

        # Add the vertical button layout to the maintenance frame layout
        maintenance_frame.setLayout(maintenance_layout)
        grid_layout.addWidget(maintenance_frame, 0, 0)

        # Update the button's state initially based on maintenance_blocks
        self.update_green_opening_button_state()
        self.update_red_opening_button_state()



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
        self.clock_label = QLabel("00:00:00")   #(myClock.format_time(0))
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
        self.speed_combo_box.addItems(["1x", "2x", "5x", "10x", "25x"])  # Example speed options
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
        self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 30px")
        self.mode_button.clicked.connect(self.mode_clicked)
        mode_layout.addWidget(self.mode_button)

        # Add Hbox for upload/dispatch buttons
        self.upload_dispatch_layout = QHBoxLayout()

        # Add the upload button for green line
        self.green_upload_button = QPushButton('Upload a Schedule for Green Line')
        self.green_upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.green_upload_button.setStyleSheet("background-color: green; color: white; font-size: 18px")
        self.green_upload_button.clicked.connect(self.green_upload_clicked)
        self.upload_dispatch_layout.addWidget(self.green_upload_button)

        # Add the upload button for red line
        self.red_upload_button = QPushButton('Upload a Schedule for Red Line')
        self.red_upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.red_upload_button.setStyleSheet("background-color: red; color: white; font-size: 18px")
        self.red_upload_button.clicked.connect(self.red_upload_clicked)
        self.upload_dispatch_layout.addWidget(self.red_upload_button)

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

        # Add widgets for dispatch rate
        self.green_rate_label = QLabel("Trains/hr")
        self.green_rate_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.green_rate_label.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        self.green_rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        dispatch_layout.addWidget(self.green_rate_label)

        self.red_rate_label = QLabel("Trains/hr")
        self.red_rate_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.red_rate_label.setStyleSheet("background-color: red; color: white; font-size: 16px;")
        self.red_rate_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        dispatch_layout.addWidget(self.red_rate_label)

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
        self.train_authority_label.setStyleSheet("background-color: #772ce8; color: white; font-size: 14px;")
        self.train_authority_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.train_data_small_layout.addWidget(self.train_authority_label)

        #Create the label for suggested speed
        self.train_suggested_speed_label = QLabel("Suggested Speed")
        self.train_suggested_speed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.train_suggested_speed_label.setStyleSheet("background-color: #772ce8; color: white; font-size: 12px;")
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

        self.label_and_switch_layout = QHBoxLayout()

        # Label for Block Occupancies
        block_occupancies_label = QLabel("Block Occupancies")
        block_occupancies_label.setStyleSheet("color: white; font-size: 20px;")
        block_occupancies_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.label_and_switch_layout.addWidget(block_occupancies_label)

        # Switch for toggling view
        self.block_occupancies_toggle = QPushButton("Toggle to Red Line")
        self.block_occupancies_toggle.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.block_occupancies_toggle.setStyleSheet("background-color: #772ce8; color: white; font-size: 12px")
        self.block_occupancies_toggle.clicked.connect(self.occupancies_view_clicked)
        self.label_and_switch_layout.addWidget(self.block_occupancies_toggle)

        blocks_layout.addLayout(self.label_and_switch_layout)

        # Create green blocks grid
        self.green_blocks_widget = QWidget()
        self.green_blocks_grid_layout = QGridLayout(self.green_blocks_widget)
        number = 1
        # Create 10x15 grid for green
        for row in range(10):
            for col in range(15):
                block_label = QLabel(str(number))  # Convert number to string for QLabel text
                block_label.setStyleSheet("background-color: green; color: white; font-size: 10px;")
                block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                self.green_blocks_grid_layout.addWidget(block_label, row, col)
                self.block_labels['Green', number] = block_label
                number += 1
        blocks_layout.addWidget(self.green_blocks_widget)

        # Create red blocks grid
        self.red_blocks_widget = QWidget()
        self.red_blocks_grid_layout = QGridLayout(self.red_blocks_widget)
        number = 1
        # Create 7x11 grid for red
        for row in range(7):
            for col in range(11):
                # Skip the last cell (row 6, column 10)
                if row == 6 and col == 10:
                    continue
                block_label = QLabel(str(number))  # Convert number to string for QLabel text
                block_label.setStyleSheet("background-color: green; color: white; font-size: 14px;")
                block_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                self.red_blocks_grid_layout.addWidget(block_label, row, col)
                self.block_labels['Red', number] = block_label
                number += 1
        blocks_layout.addWidget(self.red_blocks_widget)

        # Initially show green grid and hide red grid
        self.red_blocks_widget.hide()

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
    def green_closure_clicked(self):
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
        label = QLabel("What Block Requires Maintenance?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create Label for Line
        green_label = QLabel("Green")
        green_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        green_label.setStyleSheet("background-color: green;")
        h_layout.addWidget(green_label)

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
        button.clicked.connect(lambda: self.green_submit_closure(dialog, block_combo_box.currentText()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

        # Custom dialog for user to select maintenance closure line
    def red_closure_clicked(self):
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
        label = QLabel("What Block Requires Maintenance?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create Cbox for Line
        red_label = QLabel("Red")
        red_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        red_label.setStyleSheet("background-color: red;")
        h_layout.addWidget(red_label)

        # Create Cbox for Block
        block_combo_box = QComboBox()
        maintenance_numbers = {block[1] for block in self.maintenance_blocks}
        for i in range(1, 77):
            if i not in maintenance_numbers:
                block_combo_box.addItems([str(i)])
        h_layout.addWidget(block_combo_box)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.red_submit_closure(dialog, block_combo_box.currentText()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def green_submit_closure(self, dialog, block):
        block = int(block)
        new_block = ("Green", block)
        if new_block in self.occupied_blocks:
            print('Cannot place block under maintenance since train is occupying block')
        else:
            self.maintenance_blocks.add(("Green", block))
            print(self.maintenance_blocks)
            self.update_green_opening_button_state()

            # Change background color accordingly
            #if new_block in self.block_labels:
            block_label = self.block_labels[new_block]
            self.update_label_background()

            # Send maintenance block to wayside
            self.maintenance_blocks_dict["line"] = "Green"
            self.maintenance_blocks_dict["index"] = block
            self.maintenance_blocks_dict["maintenance"] = True
            print(self.maintenance_blocks_dict)
            while(1):
                print('closure')
                response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
                if response.status_code == 200:
                    break

            print("Block", block, "on the Green line has been closed for maintenance!")
            dialog.accept()

    # Handle the selection when 'Submit' is pressed
    def red_submit_closure(self, dialog, block):
        block = int(block)
        new_block = ("Red", block)
        if new_block in self.occupied_blocks:
            print('Cannot place block under maintenance since train is occupying block')
        else:
            self.maintenance_blocks.add(("Red", block))
            print(self.maintenance_blocks)
            self.update_red_opening_button_state()

            # Change background color accordingly
            #if new_block in self.block_labels:
            block_label = self.block_labels[new_block]
            self.update_label_background()

            # Send maintenance block to wayside
            self.maintenance_blocks_dict["line"] = "Red"
            self.maintenance_blocks_dict["index"] = block
            self.maintenance_blocks_dict["maintenance"] = True
            # while(1):
            #     print('closure')
            #     response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
            #     if response.status_code == 200:
            #         break

            print("Block", block, "on the Red line has been closed for maintenance!")
            dialog.accept()

    # The functionality for user opening a block from maintenance
    def green_opening_clicked(self):
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
        button.clicked.connect(lambda: self.green_submit_opening(dialog, line_combo_box.currentText()))
        h_layout.addWidget(button)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        dialog.setLayout(layout)
        dialog.exec()

    # The functionality for user opening a block from maintenance
    def red_opening_clicked(self):
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
        button.clicked.connect(lambda: self.red_submit_opening(dialog, line_combo_box.currentText()))
        h_layout.addWidget(button)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def green_submit_opening(self, dialog, open_block):
        block_line, block_number_str = open_block.split(" #")
        block_number = int(block_number_str)
        block = (block_line, block_number)
        self.recently_opened.add(block)
        self.maintenance_blocks.remove(block)
        print(self.maintenance_blocks)
        self.update_green_opening_button_state()

        # Change background color accordingly
        self.update_label_background()

        # Send maintenance block to wayside
        self.maintenance_blocks_dict["line"] = block_line
        self.maintenance_blocks_dict["index"] = block_number
        self.maintenance_blocks_dict["maintenance"] = False
        # while(1):
        #     print('opening')
        #     response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
        #     if response.status_code == 200:
        #         break

        print("Block", block_line, "on the", block_number, "line has been reopened from maintenance!")
        dialog.accept()  

    # Handle the selection when 'Submit' is pressed
    def red_submit_opening(self, dialog, open_block):
        block_line, block_number_str = open_block.split(" #")
        block_number = int(block_number_str)
        block = (block_line, block_number)
        self.recently_opened.add(block)
        self.maintenance_blocks.remove(block)
        print(self.maintenance_blocks)
        self.update_red_opening_button_state()

        # Change background color accordingly
        self.update_label_background()

        # Send maintenance block to wayside
        self.maintenance_blocks_dict["line"] = block_line
        self.maintenance_blocks_dict["index"] = block_number
        self.maintenance_blocks_dict["maintenance"] = False
        # while(1):
        #     print('opening')
        #     response = requests.post(URL + "/track-controller-sw/give-data/maintenance", json=self.maintenance_blocks_dict)
        #     if response.status_code == 200:
        #         break

        print("Block", block_line, "on the", block_number, "line has been reopened from maintenance!")
        dialog.accept()

    # Method to update the Opening button's state dynamically
    def update_green_opening_button_state(self):
        try:
            # Try disconnecting the clicked signal if it's already connected
            self.green_opening_button.clicked.disconnect()
        except TypeError:
            # If there's nothing to disconnect, just pass
            pass

        # Update the button's state based on whether there are maintenance blocks
        if len(self.maintenance_blocks) > 0:
            self.green_opening_button.setEnabled(True)
            self.green_opening_button.setStyleSheet("background-color: green; color: white;")
            self.green_opening_button.clicked.connect(self.green_opening_clicked)  # Enable click functionality
        else:
            self.green_opening_button.setEnabled(False)  # Disable the button
            self.green_opening_button.setStyleSheet("background-color: gray; color: white;")

    # Method to update the Opening button's state dynamically
    def update_red_opening_button_state(self):
        try:
            # Try disconnecting the clicked signal if it's already connected
            self.red_opening_button.clicked.disconnect()
        except TypeError:
            # If there's nothing to disconnect, just pass
            pass

        # Update the button's state based on whether there are maintenance blocks
        if len(self.maintenance_blocks) > 0:
            self.red_opening_button.setEnabled(True)
            self.red_opening_button.setStyleSheet("background-color: red; color: white;")
            self.red_opening_button.clicked.connect(self.red_opening_clicked)  # Enable click functionality
        else:
            self.red_opening_button.setEnabled(False)  # Disable the button
            self.red_opening_button.setStyleSheet("background-color: gray; color: white;")

    # The functionality of the user selecting the Simulation Speed of the system
    def sim_speed_selected(self, speed):
        self.sim_speed = int(speed[:-1])
        self.sim_speed_dict["sim_speed"] = self.sim_speed #myClock.sim_speed
        print("The simulation is now running at", self.sim_speed, "speed!")
        #myClock.sim_speed = int(speed[:-1])  # Extracting the numeric value from the selected string
        # Send Sim Speed
        # self.sim_speed = myClock.sim_speed
        
        print(f"sim2: {self.sim_speed}")

        response = requests.post(URL + "/train-model/receive-sim-speed", json=self.sim_speed_dict)
        response = requests.post(URL + "/train-controller/receive-sim-speed", json=self.sim_speed_dict)
        response = requests.post(URL + "/world-clock/get-sim-speed", json=self.sim_speed_dict)
        if response.status_code == 200:
            print('simulation running at', self.sim_speed)


    # The functionality of the user starting the simulation
    def operational_clicked(self):
        self.enable_clock = not self.enable_clock
        self.clock_enable_dict_dict["enable"] = self.enable_clock
        response = requests.post(URL + "/world-clock/get-clock-activate", json=self.clock_enable_dict)

        # Toggle the simulation state
        if self.enable_clock:
            print("The simulation has started!")

            self.sim_speed_dict["sim_speed"] = self.sim_speed
            response = requests.post(URL + "/train-controller/receive-sim-speed", json=self.sim_speed_dict)
            if response.status_code == 200:
                print('simulation running at', self.sim_speed)
        else:
            self.sim_speed_dict["sim_speed"] = 0
            response = requests.post(URL + "/train-controller/receive-sim-speed", json=self.sim_speed_dict)
            print("The simulation has been stopped!")

        # Update the button text to reflect the current state
        sender = self.sender()  # Get the button that triggered the event
        if self.enable_clock:
            sender.setText("Stop")  # Change the button text to "Stop" when running
            sender.setStyleSheet("background-color: red; color: white;")
        else:
            sender.setText("Start")  # Change the button text back to "Start" when stopped
            sender.setStyleSheet("background-color: green; color: white;")

        '''
        # Toggle the simulation state
        if not myClock.simulation_running:
            myClock.simulation_running = True
            myClock.elapsed_time = time.time()  # Reset start time when simulation starts
            print("The simulation has started!")

            self.sim_speed_dict["sim_speed"] = myClock.sim_speed
            while(1):
                response = requests.post(URL + "/train-controller/receive-sim-speed", json=self.sim_speed_dict)
                if response.status_code == 200:
                    print('simulation running at', myClock.sim_speed)
                    break
        else:
            myClock.simulation_running = False
            print("The simulation has been stopped!")

            self.sim_speed_dict["sim_speed"] = 0
            while(1):
                response = requests.post(URL + "/train-controller/receive-sim-speed", json=self.sim_speed_dict)
                if response.status_code == 200:
                    print('simulation running at', myClock.sim_speed)
                    break

        # Update the button text to reflect the current state
        sender = self.sender()  # Get the button that triggered the event
        if myClock.simulation_running:
            sender.setText("Stop")  # Change the button text to "Stop" when running
            sender.setStyleSheet("background-color: red; color: white;")
        else:
            sender.setText("Start")  # Change the button text back to "Start" when stopped
            sender.setStyleSheet("background-color: green; color: white;")
        '''

    # Update the clock every realtime second that passes
    '''
    def second_passed(self):
        # Only update the clock if the simulation is running
        #if myClock.simulation_running:
            # Update the clock for everybody 
        self.system_time = myClock.update_clock()

        # Update the label in UI
        self.clock_label.setText(myClock.current_time)
    '''

    def set_current_time(self, input):
        self.current_time = input
        self.update_clock()

    def update_clock(self):
        self.clock_label.setText(self.current_time)

    def set_seconds_cum(self, input):
        self.seconds_cum = input
            
    # What happens when the user presses Current Mode button
    def mode_clicked(self):        
        # Toggle the mode first
        self.automatic_mode = not self.automatic_mode

        if self.automatic_mode:
            # Switch to Automatic Mode
            self.mode_button.setText('Current Mode: Automatic Mode')
            self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 30px")

        else:
            # Switch to Manual Mode
            self.mode_button.setText('Current Mode: Manual Mode')
            self.mode_button.setStyleSheet("background-color: #772ce8; color: white; font-size: 30px")

        # Update the button states based on the new mode
        self.update_mode_button_state()

    # Method to update the Mode button's state dynamically
    def update_mode_button_state(self):
        # No need to disconnect any signals, just update the state
        if self.automatic_mode:
            
            # Delete all previous widgets to turn them into labels
            self.green_dispatch_options_layout.removeWidget(self.green_line_label)
            self.green_line_label.deleteLater()
            self.green_dispatch_options_layout.removeWidget(self.green_schedule_train_combo_box)
            self.green_schedule_train_combo_box.deleteLater()
            self.green_station_and_time_layout.removeWidget(self.green_station_select_combo_box)
            self.green_station_select_combo_box.deleteLater()
            self.green_station_and_time_layout.removeWidget(self.green_time_select_edit)
            self.green_time_select_edit.deleteLater()
            self.green_dispatch_options_layout.removeWidget(self.green_confirm_dispatch_button)
            self.green_confirm_dispatch_button.deleteLater()
            self.green_dispatch_options_layout.deleteLater()
            self.green_station_and_time_layout.deleteLater()

            self.red_dispatch_options_layout.removeWidget(self.red_line_label)
            self.red_line_label.deleteLater()
            self.red_dispatch_options_layout.removeWidget(self.red_schedule_train_combo_box)
            self.red_schedule_train_combo_box.deleteLater()
            self.red_station_and_time_layout.removeWidget(self.red_station_select_combo_box)
            self.red_station_select_combo_box.deleteLater()
            self.red_station_and_time_layout.removeWidget(self.red_time_select_edit)
            self.red_time_select_edit.deleteLater()
            self.red_dispatch_options_layout.removeWidget(self.red_confirm_dispatch_button)
            self.red_confirm_dispatch_button.deleteLater()
            self.red_dispatch_options_layout.deleteLater()
            self.red_station_and_time_layout.deleteLater()

            # Add Hbox for upload/dispatch buttons
            self.upload_buttons_layout = QHBoxLayout()

            # Add the upload button for green line
            self.green_upload_button = QPushButton('Upload a Schedule for Green Line')
            self.green_upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_upload_button.setStyleSheet("background-color: green; color: white; font-size: 18px")
            self.green_upload_button.clicked.connect(self.green_upload_clicked)
            self.upload_dispatch_layout.addWidget(self.green_upload_button)

            # Add the upload button for red line
            self.red_upload_button = QPushButton('Upload a Schedule for Red Line')
            self.red_upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.red_upload_button.setStyleSheet("background-color: red; color: white; font-size: 18px")
            self.red_upload_button.clicked.connect(self.red_upload_clicked)
            self.upload_dispatch_layout.addWidget(self.red_upload_button)

            self.upload_dispatch_layout.addLayout(self.upload_buttons_layout)

        else:
            # Delete upload buttons
            self.upload_dispatch_layout.removeWidget(self.green_upload_button)
            self.green_upload_button.deleteLater()
            self.upload_dispatch_layout.removeWidget(self.red_upload_button)
            self.red_upload_button.deleteLater()

            self.dispatch_layout = QHBoxLayout()

            # Add a Vbox Layout for all of the sub buttons for dispatching green
            self.green_dispatch_options_layout = QVBoxLayout()

            # Add the label for Green Line
            self.green_line_label = QLabel('Green Line')
            self.green_line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_line_label.setStyleSheet("background-color: green; color: white; font-size: 18px")
            self.green_line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.green_dispatch_options_layout.addWidget(self.green_line_label)

            # Add combo box for train select
            self.green_schedule_train_combo_box = QComboBox()
            self.green_schedule_train_combo_box.setPlaceholderText('Select Train')
            self.green_schedule_train_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_schedule_train_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.green_schedule_train_combo_box.addItem('New Train')
            for train in self.trains:
                self.green_schedule_train_combo_box.addItem(train.name)
            self.green_dispatch_options_layout.addWidget(self.green_schedule_train_combo_box)

            # Add Hbox for for station selection and time enterance
            self.green_station_and_time_layout = QHBoxLayout()

            # Add combo box for station selection
            self.green_station_select_combo_box = QComboBox()
            self.green_station_select_combo_box.setPlaceholderText('Select Station')
            self.green_station_select_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_station_select_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.green_station_select_combo_box.addItems(["GLENBURY OUT", "DORMONT OUT", "MT LEBANON", "POPLAR", "CASTLE SHANNON","DORMONT IN", "OVERBROOK OUT", "INGLEWOOD OUT", "CENTRAL OUT", "WHITED", "EDGEBROOK", "PIONEER", "LEBRON", "SOUTH BANK", "CENTRAL IN", "INGLEWOOD IN", "OVERBROOK IN"])
            self.green_station_and_time_layout.addWidget(self.green_station_select_combo_box)

            # Add time entrance
            self.green_time_select_edit = QLineEdit()
            self.green_time_select_edit.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.green_time_select_edit.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            time_regex = QRegularExpression(r"^(2[0-3]|[01]\d):([0-5]\d):([0-5]\d)$")
            validator = QRegularExpressionValidator(time_regex)
            self.green_time_select_edit.setValidator(validator)
            self.green_time_select_edit.setPlaceholderText("Arrival Time")
            self.green_station_and_time_layout.addWidget(self.green_time_select_edit)

            # Add station and time sections to layout
            self.green_dispatch_options_layout.addLayout(self.green_station_and_time_layout)

            # Enable Confirm button
            self.green_confirm_dispatch_button = QPushButton("Confirm")
            self.green_confirm_dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.green_confirm_dispatch_button.setStyleSheet("background-color: green; color: white; font-size: 18px;")
            self.green_confirm_dispatch_button.clicked.connect(self.green_submit_dispatch)
            self.green_dispatch_options_layout.addWidget(self.green_confirm_dispatch_button)

            self.dispatch_layout.addLayout(self.green_dispatch_options_layout)

            # Add a Vbox Layout for all of the sub buttons for dispatching green
            self.red_dispatch_options_layout = QVBoxLayout()

            # Add the label for Red Line
            self.red_line_label = QLabel('Red Line')
            self.red_line_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.red_line_label.setStyleSheet("background-color: red; color: white; font-size: 18px")
            self.red_line_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
            self.red_dispatch_options_layout.addWidget(self.red_line_label)

            # Add combo box for train select
            self.red_schedule_train_combo_box = QComboBox()
            self.red_schedule_train_combo_box.setPlaceholderText('Select Train')
            self.red_schedule_train_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.red_schedule_train_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.red_schedule_train_combo_box.addItem('New Train')
            for train in self.trains:
                self.red_schedule_train_combo_box.addItem(train.name)
            self.red_dispatch_options_layout.addWidget(self.red_schedule_train_combo_box)

            # Add Hbox for for station selection and time enterance
            self.red_station_and_time_layout = QHBoxLayout()

            # Add combo box for station selection
            self.red_station_select_combo_box = QComboBox()
            self.red_station_select_combo_box.setPlaceholderText('Select Station')
            self.red_station_select_combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.red_station_select_combo_box.setStyleSheet("color: white; background-color: #772CE8; font-size: 16px")
            self.red_station_select_combo_box.addItems(["SHADYSIDE", "HERRON AVE", "SWISSVILLE", "PENN STATION", "STEEL PLAZA", "FIRST AVE", "STATION SQUARE", "SOUTH HILLS JUNCTION"])
            self.red_station_and_time_layout.addWidget(self.red_station_select_combo_box)

            # Add time entrance
            self.red_time_select_edit = QLineEdit()
            self.red_time_select_edit.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            self.red_time_select_edit.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            time_regex = QRegularExpression(r"^(2[0-3]|[01]\d):([0-5]\d):([0-5]\d)$")
            validator = QRegularExpressionValidator(time_regex)
            self.red_time_select_edit.setValidator(validator)
            self.red_time_select_edit.setPlaceholderText("Arrival Time")
            self.red_station_and_time_layout.addWidget(self.red_time_select_edit)

            # Add station and time sections to layout
            self.red_dispatch_options_layout.addLayout(self.red_station_and_time_layout)

            # Enable Confirm button
            self.red_confirm_dispatch_button = QPushButton("Confirm")
            self.red_confirm_dispatch_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.red_confirm_dispatch_button.setStyleSheet("background-color: green; color: white; font-size: 18px;")
            self.red_confirm_dispatch_button.clicked.connect(self.red_submit_dispatch)
            self.red_dispatch_options_layout.addWidget(self.red_confirm_dispatch_button)

            self.dispatch_layout.addLayout(self.red_dispatch_options_layout)

            self.upload_dispatch_layout.addLayout(self.dispatch_layout)

    # Allow user to upload a schedule for green line
    def green_upload_clicked(self):        
        # Open file explorer on the user's device
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Microsoft Excel Worksheet (*.xlsx);")
        if file_path:
            pass            
            try:
                # Read the Excel file
                new_trains = myScheduleReader.get_green_routes(file_path, len(self.trains))
                for train in new_trains:
                    train.get_authority_from_map()
                    self.green_yard.add_authority([train.name, train.route_authorities[0]])
                    self.glenbury_out.add_authority([train.name, train.route_authorities[1]])
                    self.dormont_out.add_authority([train.name, train.route_authorities[2]])
                    self.mt_lebanon.add_authority([train.name, train.route_authorities[3]])
                    self.poplar.add_authority([train.name, train.route_authorities[4]])
                    self.castle_shannon.add_authority([train.name, train.route_authorities[5]])
                    self.mt_lebanon.add_authority([train.name, train.route_authorities[6]])
                    self.dormont_in.add_authority([train.name, train.route_authorities[7]])
                    self.glenbury_in.add_authority([train.name, train.route_authorities[8]])
                    self.overbrook_out.add_authority([train.name, train.route_authorities[9]])
                    self.inglewood_out.add_authority([train.name, train.route_authorities[10]])
                    self.central_out.add_authority([train.name, train.route_authorities[11]])
                    self.whited.add_authority([train.name, train.route_authorities[12]])
                    self.lebron.add_authority([train.name, train.route_authorities[13]])
                    self.edgebrook.add_authority([train.name, train.route_authorities[14]])
                    self.pioneer.add_authority([train.name, train.route_authorities[15]])
                    self.lebron.add_authority([train.name, train.route_authorities[16]])
                    self.whited.add_authority([train.name, train.route_authorities[17]])
                    self.south_bank.add_authority([train.name, train.route_authorities[18]])
                    self.central_in.add_authority([train.name, train.route_authorities[19]])
                    self.inglewood_in.add_authority([train.name, train.route_authorities[20]])
                    self.overbrook_in.add_authority([train.name, train.route_authorities[21]])

                for i in new_trains:
                    self.trains.append(i)
            
            except Exception as e:
                print(f"Error reading the Excel file: {e}")
        else:
            print("No file selected.")

        for station in self.green_stations:
            print(station.name, 'has authorities', station.authorities)

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

    # Allow user to upload a schedule for red line
    def red_upload_clicked(self):        
        # Open file explorer on the user's device
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Microsoft Excel Worksheet (*.xlsx);")
        if file_path:
            pass            
            try:
                # Read the Excel file
                new_trains = myScheduleReader.get_red_routes(file_path)
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

    # Process manual dispatch for green line
    def green_submit_dispatch(self):
        selected_name = self.green_schedule_train_combo_box.currentText()
        if selected_name == 'New Train': # Create a new train
            if len(self.trains) == 0:
                new_train = 'Train 0'
            else:
                new_train = 'Train '+str(len(self.trains))

            new_train = Train(new_train, 'Green')
            
            rate_string = str(len(self.trains) + 1) +' Trains/hr'
            self.green_rate_label.setText(rate_string)
            self.green_schedule_train_combo_box.addItem(new_train.name)
            
            new_train.add_stop(self.green_station_select_combo_box.currentText())
            new_train.get_authority_from_map()

            # Set time to release train from yard
            time = self.green_time_select_edit.text()
            # Split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, time.split(":"))
            time_in_seconds = hours * 3600 + minutes * 60 + seconds
            hours = int(time_in_seconds // 3600)
            minutes = int((time_in_seconds % 3600) //60)
            seconds = int(time_in_seconds % 60)
            new_train.set_first_arrival_time(time_in_seconds)
            hours = new_train.dispatch_time // 3600
            minutes = (new_train.dispatch_time % 3600) //60
            seconds = new_train.dispatch_time % 60

            # Convert authorities to tuples for a list
            auth_list = []
            for authority in new_train.route_authorities:
                auth_list.append([new_train.name, authority])
            
            # Populate the stations
            self.green_yard.add_authority(auth_list[0])
            new_train.route_authorities.popleft()
            del auth_list[0]

            for stop in new_train.station_stops:
                for station in self.green_stations:
                    if station.name == 'STATION; YARD':
                        pass
                    elif station.name == stop:
                        station.add_authority(auth_list[0])
                    else:
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

            self.dispatch_train(new_train.name, new_train.line)
        else: # Add a stop to the train
            selected_train = next((train for train in self.trains if train.name == selected_name), None)
            #selected_train.route_authorities.clear()
            selected_train.add_stop(self.green_station_select_combo_box.currentText())
            selected_train.get_authority_from_map()

    # Process manual dispatch for red line
    def red_submit_dispatch(self):
        selected_name = self.red_schedule_train_combo_box.currentText()
        if selected_name == 'New Train': # Create a new train
            if len(self.trains) == 0:
                new_train = 'Train 0'
            else:
                new_train = 'Train '+str(len(self.trains))

            new_train = Train(new_train, 'Red')
            
            rate_string = str(len(self.trains) + 1) +' Trains/hr'
            self.red_rate_label.setText(rate_string)
            self.red_schedule_train_combo_box.addItem(new_train.name)
            
            new_train.add_stop(self.red_station_select_combo_box.currentText())
            new_train.get_authority_from_map()

            # Set time to release train from yard
            time = self.red_time_select_edit.text()
            # Split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, time.split(":"))
            time_in_seconds = hours * 3600 + minutes * 60 + seconds
            hours = int(time_in_seconds // 3600)
            minutes = int((time_in_seconds % 3600) //60)
            seconds = int(time_in_seconds % 60)
            new_train.set_first_arrival_time(time_in_seconds)
            hours = new_train.dispatch_time // 3600
            minutes = (new_train.dispatch_time % 3600) //60
            seconds = new_train.dispatch_time % 60

            # Convert authorities to tuples for a list
            auth_list = []
            for authority in new_train.route_authorities:
                auth_list.append([new_train.name, authority])
            print(auth_list)

            # Populate the stations
            self.red_yard.add_authority(auth_list[0])
            new_train.route_authorities.popleft()
            del auth_list[0]
            for stop in new_train.station_stops:
                for station in self.red_stations:
                    if station.name == 'STATION; YARD':
                        pass
                    elif station.name == stop:
                        station.add_authority(auth_list[0])
                    else:
                        station.add_authority([new_train.name, -1])
            for station in self.red_stations:
                print(station.name, 'has auths', station.authorities)

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

            self.dispatch_train(new_train.name, new_train.line)
        else: # Add a stop to the train
            selected_train = next((train for train in self.trains if train.name == selected_name), None)
            #selected_train.route_authorities.clear()
            selected_train.add_stop(self.red_station_select_combo_box.currentText())
            selected_train.get_authority_from_map()
            
    # Display the correct data based on the train selected
    def train_selected(self, selected_train):
        for train in self.trains:
            if train.name == selected_train:
                my_train = train
            else:
                pass

        imperial_authority = my_train.get_authority() * 3.28084 # Convert from metric
        imperial_authority = round(imperial_authority)
        auth_str = 'Authority = '+str(imperial_authority)+' ft'
        self.train_authority_label.setText(auth_str)
        imperial_suggested_speed = my_train.get_suggested_speed() * 0.621371 # Convert from metric
        imperial_suggested_speed = round(imperial_suggested_speed)
        speed_str = 'Suggested Speed = '+str(imperial_suggested_speed)+' mph'
        self.train_suggested_speed_label.setText(speed_str)

        if my_train.line == 'Green':
            self.train_authority_label.setStyleSheet("background-color: green; color: white;")
            self.train_suggested_speed_label.setStyleSheet("background-color: green; color: white;")
        else:
            self.train_authority_label.setStyleSheet("background-color: red; color: white;")
            self.train_suggested_speed_label.setStyleSheet("background-color: red; color: white;")

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

    # Switch the occupancies view to the other line
    def occupancies_view_clicked(self):
        self.viewing_green = not self.viewing_green
        if self.viewing_green:  # Show green, hide red
            self.block_occupancies_toggle.setText("Toggle View to Red Line")
            self.green_blocks_widget.show()
            self.red_blocks_widget.hide()
        else:  # Show red, hide green
            self.block_occupancies_toggle.setText("Togggle View to Green Line")
            self.green_blocks_widget.hide()
            self.red_blocks_widget.show()


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
                    print('releasing a train from the yard')
                    self.authority_dict["line"] = "Green"
                    self.authority_dict["index"] = id
                    popped_auth = station.pop_authority()
                    self.authority_dict["authority"] = popped_auth[1]
                    for train in self.trains:
                        if train.name == popped_auth[0]:
                            train.set_current_authority(popped_auth[1])
                            if len(train.station_stops):
                                self.wayside_vision_dict["line"] = "Green"
                                self.wayside_vision_dict["index"] = 1
                                self.wayside_vision_dict["output_block"] = 0
                                # while(1):
                                #     response = requests.post(URL + "/track-controller-sw/give-data/wayside-vision", json=self.wayside_vision_dict)
                                #     if response.status_code == 200:
                                #         break
                            else:
                                self.wayside_vision_dict["line"] = "Green"
                                self.wayside_vision_dict["index"] = 1
                                self.wayside_vision_dict["output_block"] = 58
                                # while(1):
                                #     response = requests.post(URL + "/track-controller-sw/give-data/wayside-vision", json=self.wayside_vision_dict)
                                #     if response.status_code == 200:
                                #         break
                    station.set_popped(True)
                    # Send Wayside Vision
                    self.wayside_vision_dict["line"] = "Green"
                    self.wayside_vision_dict["index"] = 2
                    self.wayside_vision_dict["output_block"] = 0
                    # while(1):
                    #     response = requests.post(URL + "/track-controller-sw/give-data/authority", json=self.authority_dict)
                    #     if response.status_code == 200:
                    #         break
        
        for station in self.green_stations:
            station_id = 0
            new_block = ("Green", 0)
            if new_block in self.occupied_blocks:
                self.yard_was_occupied = False
            if new_block not in self.occupied_blocks and self.yard_was_occupied == False:
                station.set_popped(False)
                self.wayside_vision_dict["line"] = "Green"
                self.wayside_vision_dict["index"] = 2
                self.wayside_vision_dict["output_block"] = 62
                # try:
                #     response = requests.post(URL + "/track-controller-sw/give-data/wayside-vision", json=self.wayside_vision_dict)                        
                #     response.raise_for_status()  # This will raise an error for 4xx/5xx responses

                #     if response.status_code == 200:
                #         break

                # except requests.exceptions.HTTPError as http_err:
                #     # Print the HTTP error response
                #     print(f"HTTP error occurred: {http_err}")  # HTTP error details
                #     print("Response content:", response.text)   # Full response content

                # except Exception as err:
                #     # Catch any other exceptions
                #     print(f"Other error occurred: {err}")


        # Speed Stuff 
        for block in data_dict["Green"]:
            if block["speed_hazard"] == True and ("Green", block["block"]) not in self.recent_speed_hazards: # Add to speed hazard set
                # Change speed to zero
                blk = self.blocks["Green"][block["block"]]
                if blk.get_speed_hazard == True:
                    break
                self.recent_speed_hazards.add(("Green", block["block"]))
                self.suggested_speed_dict["line"] = "Green"
                self.suggested_speed_dict["index"] = block["block"]
                self.suggested_speed_dict["speed"] = 0
                for train in self.trains:
                    train.set_suggested_speed(0)
                # while(1):
                #     response = requests.post(URL + "/track-controller-sw/give-data/speed", json=self.suggested_speed_dict)
                #     if response.status_code == 200:
                #         break
            elif block["speed_hazard"] == False and ("Green", block["block"]) in self.recent_speed_hazards:
                # Change speed to actual
                self.recent_speed_hazards.remove(("Green", block["block"]))
                self.suggested_speed_dict["line"] = "Green"
                self.suggested_speed_dict["index"] = block["block"]
                blk = self.blocks["Green"][block["block"]]
                self.suggested_speed_dict["speed"] = blk.get_block_speed()
                blk.speed_hazard = True
                for train in self.trains:
                    train.set_suggested_speed(blk.get_block_speed())
                while(1):
                    response = requests.post(URL + "/track-controller-sw/give-data/speed", json=self.suggested_speed_dict)
                    if response.status_code == 200:
                        break
        
        self.update_label_background()

    # Release a train from the yard if its time
    def dispatch_train(self, name, line):
        # Put authority on the YARD block
        self.authority_dict["line"] = line
        self.authority_dict["index"] = 0
        if line == 'Green':
            popped_auth = self.green_yard.pop_authority()
        else:
            popped_auth = self.red_yard.pop_authority()
        self.authority_dict["authority"] = popped_auth[1]
        while(1):
                response = requests.post(URL + "/track-controller-sw/give-data/authority", json=self.authority_dict)
                if response.status_code == 200:
                    break
        self.wayside_vision_dict["line"] = line
        self.wayside_vision_dict["index"] = 2
        self.wayside_vision_dict["output_block"] = 0
        while(1):
            try:
                response = requests.post(URL + "/track-controller-sw/give-data/wayside-vision", json=self.wayside_vision_dict)                        
                response.raise_for_status()  # This will raise an error for 4xx/5xx responses

                if response.status_code == 200:
                    break

            except requests.exceptions.HTTPError as http_err:
                # Print the HTTP error response
                print(f"HTTP error occurred: {http_err}")  # HTTP error details
                print("Response content:", response.text)   # Full response content

            except Exception as err:
                # Catch any other exceptions
                print(f"Other error occurred: {err}")
        self.yard_was_occupied = True
        self.wayside_vision_dict["line"] = line
        self.wayside_vision_dict["index"] = 1
        self.wayside_vision_dict["output_block"] = 0
        while(1):
            response = requests.post(URL + "/track-controller-sw/give-data/wayside-vision", json=self.wayside_vision_dict)
            if response.status_code == 200:
                break
        # tell nate to create a train
        name = name[-1]
        index = int(name)
        self.train_initializer_dict["line"] = line
        self.train_initializer_dict["id"] = index
        print('Current Train is', index)
        while(1):
            try:
                response = requests.post(URL + "/track-model/make-train", json=self.train_initializer_dict)
                if response.status_code == 200:
                    break
                else:
                    requests.get('http://127.0.0.1:5000/shutdown')
                    sys.exit()
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                print("Response Content: ", response.text)
            except Exception as err:
                print(f"Other error Occurred: {err}")
            
        self.trains[0].on_track = True

if __name__ == "__main__":    

    app = QApplication(sys.argv)

    # Create an object from the ScheduleReader class
    myScheduleReader = ScheduleReader()

    window = MyWindow()
    window.show()

    sys.exit(app.exec())