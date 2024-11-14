import sys
import os
import shutil
import sys
import os
import shutil
import json
import copy
import requests  # For triggering shutdown
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QComboBox, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

LOCAL_DEVELOPMENT = False
base_path = os.path.dirname(__file__)

try:
    # For Launcher
    from TrackController.Components.Toggle_Buttons.AutoToggle import AutoToggle
    from TrackController.Components.Toggle_Buttons.ModeToggle import ModeToggle
    from TrackController.Components.Switches.Switches import Switches
    from TrackController.Components.Traffic_Lights.TrafficLights import TrafficLights
    from TrackController.Components.Crossings.Crossings import Crossings
    from TrackController.Components.Block_Occupancy.block_occupancy import BlockOccupancy
    from TrackController.Components.PLC_Manager import PLCManager
except ImportError:
    # For Local
    LOCAL_DEVELOPMENT = True
    from Components.Toggle_Buttons.AutoToggle import AutoToggle
    from Components.Toggle_Buttons.ModeToggle import ModeToggle
    from Components.Switches.Switches import Switches
    from Components.Traffic_Lights.TrafficLights import TrafficLights
    from Components.Crossings.Crossings import Crossings
    from Components.Block_Occupancy.block_occupancy import BlockOccupancy
    from Components.PLC_Manager import PLCManager

# Load the JSON file with block and switch data
json_path=f"{base_path}/track_model.json"
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

        self.plc_managers = {}
        self.plc_num = 0
        # self.blue_line_plc_manager = PLCManager(self.data_test["Blue"]["SW"], self.auto)
        # self.blue_line_plc_manager_HW = PLCManager(self.data_test["Blue"]["HW"], self.auto)

        with open(f"{base_path}/styles.qss", "r") as f:
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

        if LOCAL_DEVELOPMENT == False:
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
            print("Failed to retrieve occupancies from Track Model:", response.text)
            return

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
        if response.status_code != 200:
            print("Failed to give signals to Track Model")

    def get_block_data(self):
        data = {
            "Green": self.data_main["Green"]["SW"]["blocks"],
            "Red": self.data_main["Red"]["SW"]["blocks"]
        }
        return data

    def add_maintenance(self, maintenance):
        response = requests.post("http://127.0.0.1:5000/track-model/set-maintenance", json=maintenance)
        if response.status_code != 200:
            print("Failed to give maintenance to Track Model")
        
    
    def add_authority(self, authority):
        # TODO:
        # send the authority to the Track Model
        print("Got em")
        print(authority)

        # response = requests.post("http://127.0.0.1:5000/track-model/set-authority", json=authority)
        # if response.status_code != 200:
        #     print("Failed to give authority to Track Model")

    def add_speed(self, speed):
        # TODO:
        # send the speed to the Track Model
        print("Got em")
        print(speed)

        # response = requests.post("http://127.0.0.1:5000/track-model/set-speed", json=speed)
        # if response.status_code != 200:
        #     print("Failed to give speed to Track Model")

    def add_wayside_vision(self, vision):
        print("Got em")
        print(vision)

        if vision["index"] == 1:
            if vision["output_block"] == 58:
                self.data_main["Green"]["SW"]["switches"][0]["suggested_toggle"] = True
            elif vision["output_block"] == 0:
                self.data_main["Green"]["SW"]["switches"][0]["suggested_toggle"] = False
        elif vision["index"] == 2:
            if vision["output_block"] == 0:
                self.data_main["Green"]["SW"]["switches"][1]["suggested_toggle"] = True
            elif vision["output_block"] == 62:
                self.data_main["Green"]["SW"]["switches"][1]["suggested_toggle"] = False


    def closeEvent(self, event):
        """Override the close event to stop the timer before closing."""
        for name, plc_manager in self.plc_managers.items():
            plc_manager.stop_current_plc()  # Call the member function on each instance

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
        file_label = QLabel("No PLC file uploaded")
        left_layout.addWidget(file_label)

        # Create a horizontal layout for the upload button and the combo box
        horizontal_layout = QHBoxLayout()

        # Create an upload button
        upload_button = QPushButton("+")  # Set the button text to a plus sign
        upload_button.setFixedSize(100, 40)  # Adjust the size to make the plus sign more prominent

        # Style the button to center the plus symbol and make it look larger
        upload_button.setStyleSheet("font-size: 20px;")

        # Connect the button to the upload_file function
        upload_button.clicked.connect(lambda: self.upload_file(file_label))
        horizontal_layout.addWidget(upload_button)  # Add upload button to the horizontal layout

        # Create a drop-down (combo box) with values 0 and 1
        plc_dropdown = QComboBox()
        plc_dropdown.addItems(["0", "1"])  # Add options "0" and "1"
        plc_dropdown.setCurrentText(str(self.plc_num))
        plc_dropdown.setFixedSize(50, 40)  # Adjust size to match the button's height
        horizontal_layout.addWidget(plc_dropdown)
        
        left_layout.addLayout(horizontal_layout)


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
        traffic_lights_widget = TrafficLights((self.data_test if test else self.data_main), self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
        traffic_lights_scroll.setWidget(traffic_lights_widget)
        traffic_lights_scroll.setWidgetResizable(True)
        right_layout.addWidget(traffic_lights_scroll)

        # Add label for Switches
        right_layout.addWidget(QLabel("Switches"))

        # Scroll area for switches (right side)
        switches_scroll = QScrollArea()
        switches_widget = Switches((self.data_test if test else self.data_main), self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
        switches_scroll.setWidget(switches_widget)
        switches_scroll.setWidgetResizable(True)
        right_layout.addWidget(switches_scroll)

        # Add label for Crossings
        right_layout.addWidget(QLabel("Crossings"))

        # Scroll area for crossings (right side)
        crossings_scroll = QScrollArea()
        crossings_widget = Crossings((self.data_test if test else self.data_main), self.line, self.mode, self.plc_num)
        crossings_scroll.setWidget(crossings_widget)
        crossings_scroll.setWidgetResizable(True)
        right_layout.addWidget(crossings_scroll)

        # Connect dropdown menu to update content function
        lines_dropdown_menu.currentIndexChanged.connect(lambda: self.update_line(lines_dropdown_menu))
        plc_dropdown.currentIndexChanged.connect(lambda: self.update_plc_num(plc_dropdown))

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

         # Create input field
        command_speed_input_field = QLineEdit()
        command_speed_input_field.setPlaceholderText("Enter Speed Hazard (bool)...")
        command_speed_input_field.setFixedHeight(30)  # Adjusted input field height
        command_speed_input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
        input_layout_in_frame.addWidget(command_speed_input_field)
        command_speed_save_button = QPushButton("Save Speed Hazard")
        command_speed_save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
        command_speed_save_button.clicked.connect(lambda: self.save_value(block_id_input.text(),command_speed_input_field.text(), 4))
        input_layout_in_frame.addWidget(command_speed_save_button)

        # Add the input layout to the test layout
        test_layout.addLayout(input_layout_in_frame)

        # Create and add the shared content (similar to main tab but editable)
        test_content = self.create_shared_content(test=True)
        test_layout.addWidget(test_content)

        self.tabs.addTab(self.test_tab, "Test")

    def upload_file(self, file_label):
        """Handles the file upload process, saves the file to a folder, and restarts the PLC program."""
        global plc_thread, plc_stop_event
        
        tab = self.tabs.tabText(self.tabs.currentIndex())

        # Open a file dialog to select a Python script
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Python Script", "", "Python Files (*.py)")

        # Check if a file was selected
        if file_path:
            # Specify the folder where the uploaded file will be saved
            save_folder = "./uploaded_scripts"
            os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Extract the file name from the file path
            file_name = os.path.basename(file_path)
            new_file_name = f"{self.line}_line_{self.mode}_{tab}_{self.plc_num}_PLC.py"
            # Set the destination path (in the 'uploaded_scripts' folder)
            destination = os.path.join(save_folder, new_file_name)

            # Copy the selected file to the destination folder
            shutil.copy(file_path, destination)

            # Update the label to show the uploaded file path
            file_label.setText(f"Uploaded: {file_name}")

            # check if there is already a plc manager for it. If not create one
            if f"{self.line}_{self.mode}_{tab}_{self.plc_num}" not in self.plc_managers:
                if tab == "Test":
                    self.plc_managers[f"{self.line}_{self.mode}_{tab}_{self.plc_num}"] = PLCManager(self.data_test, self.line, self.mode, self.auto, self.plc_num)
                elif tab == "Main":
                    self.plc_managers[f"{self.line}_{self.mode}_{tab}_{self.plc_num}"] = PLCManager(self.data_main, self.line, self.mode, self.auto, self.plc_num)

            # Start the new PLC program
            plc_manager = self.plc_managers[f"{self.line}_{self.mode}_{tab}_{self.plc_num}"]
            plc_manager.start_new_plc(destination)
    
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
                traffic_lights.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
            
            crossings = self.test_tab.findChild(Crossings)
            if crossings:
                crossings.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
            
            switches = self.test_tab.findChild(Switches)
            if switches:
                switches.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))

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
                traffic_lights.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
            crossings = self.main_tab.findChild(Crossings)
            if crossings:
                crossings.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))
            switches = self.main_tab.findChild(Switches)
            if switches:
                switches.refresh(self.line, self.mode, self.plc_num, editable=(False if self.auto else True))

    # Swtich between lines
    def update_line(self, dropdown):
        self.line = dropdown.currentText()
        # self.update_content()

    def update_plc_num(self, dropdown):
        self.plc_num = int(dropdown.currentText())
        # self.update_content()

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
        
        for name, plc_manager in self.plc_managers.items():
            plc_manager.update_auto(self.auto)  # Call the member function on each instance

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
            for switch in self.data_test[self.line][self.mode]['switches']:
                if switch["from"] == block_id:
                    print("Updating Switch Suggestion Internally: {Block_id: " + str(block_id) + ", Switch_Suggest_State: " + text + "}")
                    switch["suggested_toggle"] = bool(int(text))
                    break
        elif index == 4:
            print("Updating Speed Hazard Internally: {Block_id: " + str(block_id) + ", state: " + text + "}")
            if text == "True" or text == "true":
                for block in self.data_test[self.line][self.mode]["blocks"]:
                    if block["block"] == block_id:
                        block["speed_hazard"] = True
                        print("set speed hazard to True")
                        break
            if text == "False" or text == "false":
                for block in self.data_test[self.line][self.mode]["blocks"]:
                    if block["block"] == block_id:
                        block["speed_hazard"] = False
                        print("set speed hazard to False")
                        break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())