import sys
import os
import shutil
import sys
import os
import shutil
import json
import copy
from threading import Thread
import requests  # For triggering shutdown
#from TrackController.api import start_api  # Import the API starter function
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QComboBox, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from TrackController.Components.Toggle_Buttons.AutoToggle import AutoToggle
from TrackController.Components.Toggle_Buttons.ModeToggle import ModeToggle
from TrackController.Components.Switches.Switches import Switches
from TrackController.Components.Traffic_Lights.TrafficLights import TrafficLights
from TrackController.Components.Crossings.Crossings import Crossings
from TrackController.Components.Block_Occupancy.block_occupancy import BlockOccupancy
from TrackController.Components.PLC_Manager import PLCManager


# Load the JSON file with block and switch data
json_path="TrackController/track_model.json"
with open(json_path, 'r') as json_file:
    data = json.load(json_file)

lines = ["Blue", "Green", "Red"]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initial properties of the UI
        self.line = "Green"
        self.mode = "SW"
        self.auto = True
        self.data_main = copy.deepcopy(data)
        self.data_test = copy.deepcopy(data)

        self.sw_signal_data = {
            "Green": {
                "switches": self.data_main["Green"]["SW"]["switches"],
                "traffic_lights": self.data_main["Green"]["SW"]["traffic_lights"],
                "crossings": self.data_main["Green"]["SW"]["crossings"]
            },
            "Red": {
                "switches": self.data_main["Red"]["SW"]["switches"],
                "traffic_lights": self.data_main["Red"]["SW"]["traffic_lights"],
                "crossings": self.data_main["Red"]["SW"]["crossings"]
            }
        }

        self.maintence_list = []
        self.authority_list = []
        self.speed_list = []
        self.wayside_vision = []

        self.blue_line_plc_manager = PLCManager(self.data_test["Blue"]["SW"], self.auto)
        self.blue_line_plc_manager_HW = PLCManager(self.data_test["Blue"]["HW"], self.auto)

        with open("TrackController/styles.qss", "r") as f:
            style = f.read()
        self.setStyleSheet(style)

        # Set window geometry
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.setGeometry(0, 0, self.screen_width // 2, self.screen_height)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, self.screen_width // 2, self.screen_height)

        self.create_main_tab()
        self.create_test_tab()
        self.tabs.currentChanged.connect(self.update_content)

        # Create a QTimer instance
        self.update_ui_timer = QTimer(self)
        # Connect the timer's timeout signal to the update_content method
        self.update_ui_timer.timeout.connect(self.update_content)
        # Start the timer to call update_content every 500 milliseconds
        self.update_ui_timer.start(500)

        self.api_call_timer = QTimer(self)
        self.api_call_timer.timeout.connect(self.call_apis)
        self.api_call_timer.start(1000)

    def call_apis(self):
        self.request_block_occupancies()
        self.give_signals()

    def request_block_occupancies(self):
        response = requests.get("http://127.0.0.1:5000/track-model/get-data/occupancies")
        data_dict = {} # Initialize outside of if statemnt scope

        if response.status_code == 200:
            data_dict = response.json()  # This converts the JSON response to a Python dictionary
        else:
            print("Failed to retrieve data:", response.text)
            return
        
        # print("Updating block occupancies")
        # Green
        for block in self.data_main["Green"]["HW"]["blocks"]:
            block["occupied"] = data_dict['Green'][block["block"]]
        for block in self.data_main["Green"]["SW"]["blocks"]:
            block["occupied"] = data_dict['Green'][block["block"]]

        # Red
        # for block in self.data_main["Red"]["HW"]["blocks"]:
        #     block["toggled"] = data_dict['Red'][block["block"]]
        # for block in self.data_main["Red"]["SW"]["blocks"]:
        #     block["toggled"] = data_dict['Red'][block["block"]]
    
    def give_signals(self):
        response = requests.post("http://127.0.0.1:5000/track-model/recieve-signals", json=self.sw_signal_data)

    def get_block_data(self):
        data = {
            # "Blue": self.data_test["Blue"]["SW"]["blocks"],
            "Green": self.data_main["Green"]["SW"]["blocks"],
            "Red": self.data_main["Red"]["SW"]["blocks"]
        }

        return data

    def add_maintenance(self, maintenance):
        # self.maintence_list.append(maintenance)
        response = requests.post("http://127.0.0.1:5000/track-model/set-maintenance", json=maintenance)
        
    
    def add_authority(self, authority):
        self.authority_list.append(authority)
        
        # TODO:
        # send the authority to the Track Model

    def add_speed(self, speed):
        self.speed_list.append(speed)
        
        # TODO:
        # send the speed to the Track Model

    def add_wayside_vision(self, vision):
        self.wayside_vision.append(vision)

        # TODO:
        # parse and give it to the waysides

    def closeEvent(self, event):
        """Override the close event to stop the timer before closing."""
        self.blue_line_plc_manager.stop_current_plc()  # Stop the PLC if running
        self.blue_line_plc_manager_HW.stop_current_plc()  # Stop the PLC if running
        self.update_ui_timer.stop()  # Stop the timer when the app closes
        event.accept()  # Accept the event to close the window
        
    def create_shared_content(self, test=False):
        tab_widget = QWidget()

        # Main layout for the entire tab
        main_layout = QHBoxLayout(tab_widget)

        # Left side layout for Block Occupancy and Dropdown Menu
        left_layout = QVBoxLayout()

        # Create dropdown menu for line selection
        lines_dropdown_menu = QComboBox()
        lines_dropdown_menu.addItems(["Blue", "Green", "Red"])
        lines_dropdown_menu.setFixedHeight(40)  # Adjust height for a consistent look
        lines_dropdown_menu.setCurrentText(self.line)
        left_layout.addWidget(lines_dropdown_menu)

        # Create a label to show the uploaded file path
        file_label = QLabel("No file uploaded")
        left_layout.addWidget(file_label)

        # Create an upload button
        upload_button = QPushButton("+")  # Set the button text to a plus sign
        upload_button.setFixedSize(100, 40)  # Adjust the size to make the plus sign more prominent

        # Style the button to center the plus symbol and make it look larger
        upload_button.setStyleSheet("font-size: 20px;")

        # Connect the button to the upload_file function
        upload_button.clicked.connect(lambda: self.upload_file(file_label))
        left_layout.addWidget(upload_button, stretch=1)

        # Add label for Block Occupancy
        left_layout.addWidget(QLabel("Block Occupancy"))

        # Create scroll area for block occupancy (left side)
        block_scroll = QScrollArea()
        block_scroll_widget = BlockOccupancy((self.data_test if test else self.data_main), self.line, self.mode, test)
        block_scroll.setWidget(block_scroll_widget)
        block_scroll.setWidgetResizable(True)
        left_layout.addWidget(block_scroll, stretch=4)

        # Right side layout for buttons (traffic lights, switches, crossings)
        right_layout = QVBoxLayout()

        # Add HW/SW toggle button
        hw_sw_toggle_button = ModeToggle(self.mode)
        right_layout.addWidget(hw_sw_toggle_button)

        # Add Manual/Auto toggle button
        manual_auto_toggle_button = AutoToggle(self.auto)
        right_layout.addWidget(manual_auto_toggle_button)

        # Add label for Traffic Lights
        right_layout.addWidget(QLabel("Traffic Lights"))

        # Scroll area for traffic lights (right side)
        traffic_lights_scroll = QScrollArea()
        traffic_lights_widget = TrafficLights((self.data_test if test else self.data_main), self.line, self.mode, editable=(False if self.auto else True))
        traffic_lights_scroll.setWidget(traffic_lights_widget)
        traffic_lights_scroll.setWidgetResizable(True)
        right_layout.addWidget(traffic_lights_scroll)

        # Add label for Switches
        right_layout.addWidget(QLabel("Switches"))

        # Scroll area for switches (right side)
        switches_scroll = QScrollArea()
        switches_widget = Switches((self.data_test if test else self.data_main), self.line, self.mode, editable=(False if self.auto else True))
        switches_scroll.setWidget(switches_widget)
        switches_scroll.setWidgetResizable(True)
        right_layout.addWidget(switches_scroll)

        # Add label for Crossings
        right_layout.addWidget(QLabel("Crossings"))

        # Scroll area for crossings (right side)
        crossings_scroll = QScrollArea()
        crossings_widget = Crossings((self.data_test if test else self.data_main), self.line, self.mode)
        crossings_scroll.setWidget(crossings_widget)
        crossings_scroll.setWidgetResizable(True)
        right_layout.addWidget(crossings_scroll)

        # Connect dropdown menu to update content function
        lines_dropdown_menu.currentIndexChanged.connect(lambda: self.update_line(lines_dropdown_menu))

        # hw_sw_toggle_button.clicked.connect(self.toggle_hw_sw_mode)
        manual_auto_toggle_button.clicked.connect(self.toggle_manual_auto_mode)

        # Add left and right layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        return tab_widget
    
    def create_main_tab(self):
        self.main_tab = self.create_shared_content(test=False)
        self.tabs.addTab(self.main_tab, "Main")

    def create_test_tab(self):
        self.test_tab = QWidget()
        test_layout = QHBoxLayout(self.test_tab)

        # Create a frame to contain the input section
        input_frame = QFrame()
        input_frame.setFixedWidth(self.screen_width // 6)  # Set a smaller width for the input section
        input_frame.setFixedHeight(300)  # Increased height for input section to prevent overlap
        test_layout.addWidget(input_frame)

        # Input layout inside the frame
        input_layout_in_frame = QVBoxLayout(input_frame)
        input_layout_in_frame.setSpacing(10)  # Reduced spacing between input fields and buttons

        # Create input fields and save buttons
        labels = ["Authority", "Suggested Speed", "Switch Suggested", "Commanded Speed"]

        # Create input field
        block_id_input = QLineEdit()
        block_id_input.setPlaceholderText(f"Enter block id...")
        block_id_input.setFixedHeight(30)  # Adjusted input field height
        block_id_input.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(block_id_input)

        # Add a spacer item below the input field to create space
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(40)  # Set the height of the spacer
        input_layout_in_frame.addWidget(spacer_widget)
        
        # Create input field
        authority_input_field = QLineEdit()
        authority_input_field.setPlaceholderText("Enter Authority (meters) ...")
        authority_input_field.setFixedHeight(30)  # Adjusted input field height
        authority_input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(authority_input_field)
        authority_save_button = QPushButton("Save Authority")
        authority_save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
        authority_save_button.clicked.connect(lambda: self.save_value(block_id_input.text(), authority_input_field.text(), 0))
        input_layout_in_frame.addWidget(authority_save_button)

        # Create input field
        suggest_speed_input_field = QLineEdit()
        suggest_speed_input_field.setPlaceholderText("Enter Suggested Speed (km/hr) ...")
        suggest_speed_input_field.setFixedHeight(30)  # Adjusted input field height
        suggest_speed_input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(suggest_speed_input_field)
        suggest_speed_save_button = QPushButton("Save Suggested Speed")
        suggest_speed_save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
        suggest_speed_save_button.clicked.connect(lambda: self.save_value(block_id_input.text(), suggest_speed_input_field.text(), 1))
        input_layout_in_frame.addWidget(suggest_speed_save_button)

        # Create input field
        switch_suggest_input_field = QLineEdit()
        switch_suggest_input_field.setPlaceholderText("Enter Switch Suggestion (0 or 1) ...")
        switch_suggest_input_field.setFixedHeight(30)  # Adjusted input field height
        switch_suggest_input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(switch_suggest_input_field)
        switch_suggest_save_button = QPushButton("Save Switch Suggestion")
        switch_suggest_save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
        switch_suggest_save_button.clicked.connect(lambda: self.save_value(block_id_input.text(), switch_suggest_input_field.text(), 2))
        input_layout_in_frame.addWidget(switch_suggest_save_button)

         # Create input field
        command_speed_input_field = QLineEdit()
        command_speed_input_field.setPlaceholderText("Enter Commanded Speed (km/hr) ...")
        command_speed_input_field.setFixedHeight(30)  # Adjusted input field height
        command_speed_input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(command_speed_input_field)
        command_speed_save_button = QPushButton("Save Commanded Speed")
        command_speed_save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
        command_speed_save_button.clicked.connect(lambda: self.save_value(block_id_input.text(),command_speed_input_field.text(), 3))
        input_layout_in_frame.addWidget(command_speed_save_button)

        # Add the input layout to the test layout
        test_layout.addLayout(input_layout_in_frame)

        # Create and add the shared content (similar to main tab but editable)
        test_content = self.create_shared_content(test=True)
        test_layout.addWidget(test_content)

        self.tabs.addTab(self.test_tab, "Test")

    #def create_upload_tab(self):
    #    """Creates an upload tab and adds it to the provided QTabWidget."""
        # Create the upload tab widget
        #upload_tab = QWidget()
        #upload_layout = QVBoxLayout()
        
        # Create dropdown menu for line selection
        #lines_dropdown_menu = QComboBox()
        #lines_dropdown_menu.addItems(["Blue", "Green", "Red"])
        #lines_dropdown_menu.setFixedHeight(40)  # Adjust height for a consistent look
        #lines_dropdown_menu.setFixedWidth(120)  # Adjust height for a consistent look
        #lines_dropdown_menu.setCurrentText(self.line)
        #lines_dropdown_menu.currentIndexChanged.connect(lambda: self.update_line(lines_dropdown_menu))

        # Create a label to show the uploaded file path
        #file_label = QLabel("No file uploaded")
        
        # Create an upload button
        #upload_button = QPushButton("+")  # Set the button text to a plus sign
        #upload_button.setFixedSize(40, 100)  # Adjust the size to make the plus sign more prominent

        # Style the button to center the plus symbol and make it look larger
        #upload_button.setStyleSheet("font-size: 20px;")

        # Connect the button to the upload_file function
        #upload_button.clicked.connect(lambda: self.upload_file(file_label))

        # Add the label and button to the layout
        #upload_layout.addWidget(upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        #upload_layout.addWidget(file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set alignment for the entire layout to center
        #upload_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the layout for the upload tab
        #upload_tab.setLayout(upload_layout)

        # Add the upload tab to the provided tab widget
        #self.tabs.addTab(upload_tab, "Upload Tab")

    def upload_file(self, file_label):
        """Handles the file upload process, saves the file to a folder, and restarts the PLC program."""
        global plc_thread, plc_stop_event

        # Open a file dialog to select a Python script
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Python Script", "", "Python Files (*.py)")

        # Check if a file was selected
        if file_path:
            # Specify the folder where the uploaded file will be saved
            save_folder = "./uploaded_scripts"
            os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Extract the file name from the file path
            file_name = os.path.basename(file_path)
            new_file_name = self.line + "_line_PLC.py"
            # Set the destination path (in the 'uploaded_scripts' folder)
            destination = os.path.join(save_folder, new_file_name)

            # Copy the selected file to the destination folder
            shutil.copy(file_path, destination)

            # Update the label to show the uploaded file path
            file_label.setText(f"Uploaded: {file_name}")

            # Start the new PLC program
            if self.line == "Blue":
                self.blue_line_plc_manager.start_new_plc(destination)
            elif self.line == "Green":
                pass
            elif self.line == "Red":
                pass
    
    # Function to update content when switching lines, mode, or Auto/Manual
    def update_content(self):
        current_tab_index = self.tabs.currentIndex()
        
        if self.tabs.tabText(current_tab_index) == "Test":
            dropdown = self.test_tab.findChild(QComboBox)
            if dropdown:
                dropdown.setCurrentText(self.line)
            
            hw_sw_btn = self.test_tab.findChild(ModeToggle)
            if hw_sw_btn:
                hw_sw_btn.refresh(self.mode)
            
            man_auto_btn = self.test_tab.findChild(AutoToggle)
            if man_auto_btn:
                man_auto_btn.refresh(self.auto)

            block_occupancy = self.test_tab.findChild(BlockOccupancy)
            if block_occupancy:
                block_occupancy.refresh(self.line, self.mode, editable=True)

            traffic_lights = self.test_tab.findChild(TrafficLights)
            if traffic_lights:
                traffic_lights.refresh(self.line, self.mode, editable=(False if self.auto else True))
            
            crossings = self.test_tab.findChild(Crossings)
            if crossings:
                crossings.refresh(self.line, self.mode, editable=(False if self.auto else True))
            
            switches = self.test_tab.findChild(Switches)
            if switches:
                switches.refresh(self.line, self.mode, editable=(False if self.auto else True))

        if self.tabs.tabText(current_tab_index) == "Main":
            dropdown = self.main_tab.findChild(QComboBox)
            if dropdown:
                dropdown.setCurrentText(self.line)
            
            hw_sw_btn = self.main_tab.findChild(ModeToggle)
            if hw_sw_btn:
                hw_sw_btn.refresh(self.mode)
            
            man_auto_btn = self.main_tab.findChild(AutoToggle)
            if man_auto_btn:
                man_auto_btn.refresh(self.auto)
            
            dropdown = self.main_tab.findChild(QComboBox)
            if dropdown:
                dropdown.setCurrentText(self.line)

            block_occupancy = self.main_tab.findChild(BlockOccupancy)
            if block_occupancy:
                block_occupancy.refresh(self.line, self.mode, editable=False)

            traffic_lights = self.main_tab.findChild(TrafficLights)
            if traffic_lights:
                traffic_lights.refresh(self.line, self.mode, editable=(False if self.auto else True))
            crossings = self.main_tab.findChild(Crossings)
            if crossings:
                crossings.refresh(self.line, self.mode, editable=(False if self.auto else True))
            switches = self.main_tab.findChild(Switches)
            if switches:
                switches.refresh(self.line, self.mode, editable=(False if self.auto else True))

    # Swtich between lines
    def update_line(self, dropdown):
        self.line = dropdown.currentText()
        self.update_content()

    # Toggle between Hardware and Software modes
    # def toggle_hw_sw_mode(self):
    #    if self.mode == "HW":
    #        self.mode = "SW"
    #    else:
    #        self.mode = "HW"
    #   self.update_content()

    # Toggle between Manual and Auto modes
    def toggle_manual_auto_mode(self):
        if self.auto == True:
            self.auto = False
        else:
            self.auto = True
        self.blue_line_plc_manager.update_auto(self.auto)
        self.update_content()

    def save_value(self, block_id, text, index):
        if block_id == "" or text == "":
            return
        try:
            block_id = int(block_id)
        except Exception as e:
            print("Error converting block_id to int: " + e)
            return

        if index == 0:
            print("Sending Authority to Track Model: {Block_id: " + str(block_id) + ", Meters: " + text + "}" )
        elif index == 1 or index == 3:
            print("Sending Suggested/Commanded Speed to Track Model: {Block_id: " + str(block_id) + ", Speed(kh/hr): " + text + "}")
        elif index == 2:
            print("Updating Switch Suggestion Internally: {Block_id: " + str(block_id) + ", Switch_Suggest_State: " + text + "}")
            for switch in self.data_test[self.line][self.mode]['switches']:
                if switch["from"] == block_id:
                    switch["suggested_toggle"] = bool(int(text))
                    break


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     ex.show()
#     sys.exit(app.exec())