import sys
import os
import shutil
import json
import copy
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QComboBox, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from Components.Toggle_Buttons.AutoToggle import AutoToggle
from Components.Toggle_Buttons.ModeToggle import ModeToggle
from Components.Switches.Switches import Switches
from Components.Traffic_Lights.TrafficLights import TrafficLights
from Components.Crossings.Crossings import Crossings
from Components.Block_Occupancy.block_occupancy import BlockOccupancy

# Load the JSON file with block and switch data
with open('track_model.json', 'r') as json_file:
    data = json.load(json_file)

lines = ["Blue", "Green", "Red"]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initial properties of the UI
        self.line = "Blue"
        self.mode = "HW"
        self.auto = True
        self.data_main = copy.deepcopy(data)
        self.data_test = copy.deepcopy(data)
        self.saved_values = []  # List to store saved input values

        with open("styles.qss", "r") as f:
            style = f.read()
        app.setStyleSheet(style)

        # Set window geometry
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.setGeometry(0, 0, self.screen_width // 2, self.screen_height)

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, self.screen_width // 2, self.screen_height)

        self.create_main_tab()
        self.create_test_tab()
        self.create_upload_tab()
        self.tabs.currentChanged.connect(self.update_content)

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

        # Add label for Block Occupancy
        left_layout.addWidget(QLabel("Block Occupancy"))

        # Create scroll area for block occupancy (left side)
        block_scroll = QScrollArea()
        block_scroll_widget = BlockOccupancy((self.data_test if test else self.data_main), self.line, self.mode, test)
        block_scroll.setWidget(block_scroll_widget)
        block_scroll.setWidgetResizable(True)
        left_layout.addWidget(block_scroll)

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

        hw_sw_toggle_button.clicked.connect(self.toggle_hw_sw_mode)
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
        labels = ["Authority", "Suggested Speed", "Switch Bool", "Commanded Speed"]

        for idx in range(len(labels)):
            # Create input field
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {labels[idx].lower()}...")
            input_field.setFixedHeight(30)  # Adjusted input field height
            input_field.setMinimumWidth(150)  # Ensure input field has a minimum width
            input_layout_in_frame.addWidget(input_field)

            # Create save button
            save_button = QPushButton(f"Save {labels[idx]}", clicked=lambda idx=idx: self.save_value(input_field.text(), idx))
            save_button.setFixedHeight(30)  # Ensure save button doesn't overlap
            input_layout_in_frame.addWidget(save_button)

        # Add the input layout to the test layout
        test_layout.addLayout(input_layout_in_frame)

        # Create and add the shared content (similar to main tab but editable)
        test_content = self.create_shared_content(test=True)
        test_layout.addWidget(test_content)

        self.tabs.addTab(self.test_tab, "Test")

    def create_upload_tab(self):
        """Creates an upload tab and adds it to the provided QTabWidget."""
        # Create the upload tab widget
        upload_tab = QWidget()
        upload_layout = QVBoxLayout()
        
        # Create dropdown menu for line selection
        lines_dropdown_menu = QComboBox()
        lines_dropdown_menu.addItems(["Blue", "Green", "Red"])
        lines_dropdown_menu.setFixedHeight(40)  # Adjust height for a consistent look
        lines_dropdown_menu.setFixedWidth(120)  # Adjust height for a consistent look
        lines_dropdown_menu.setCurrentText(self.line)
        lines_dropdown_menu.currentIndexChanged.connect(lambda: self.update_line(lines_dropdown_menu))

        # Create a label to show the uploaded file path
        file_label = QLabel("No file uploaded")
        
        # Create an upload button
        upload_button = QPushButton("+")  # Set the button text to a plus sign
        upload_button.setFixedSize(100, 100)  # Adjust the size to make the plus sign more prominent

        # Style the button to center the plus symbol and make it look larger
        upload_button.setStyleSheet("font-size: 40px;")

        # Connect the button to the upload_file function
        upload_button.clicked.connect(lambda: self.upload_file(file_label))

        # Add the label and button to the layout
        upload_layout.addWidget(lines_dropdown_menu, alignment=Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        upload_layout.addWidget(file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set alignment for the entire layout to center
        upload_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the layout for the upload tab
        upload_tab.setLayout(upload_layout)

        # Add the upload tab to the provided tab widget
        self.tabs.addTab(upload_tab, "Upload Tab")

    def upload_file(self, file_label):
        """Handles the file upload process and saves the file to a folder."""
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
    def toggle_hw_sw_mode(self):
        if self.mode == "HW":
            self.mode = "SW"
        else:
            self.mode = "HW"
        self.update_content()

    # Toggle between Manual and Auto modes
    def toggle_manual_auto_mode(self):
        if self.auto == True:
            self.auto = False
        else:
            self.auto = True
        self.update_content()

    def save_value(self, text, index):
        # Ensure the saved_values list has at least the needed number of elements
        while len(self.saved_values) <= index:
            self.saved_values.append(None)
        self.saved_values[index] = text
        print(f"Saved value at index {index}: {text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())