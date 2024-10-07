import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QComboBox, QVBoxLayout, QScrollArea, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QCheckBox
from PyQt6.QtCore import QMargins
from ModeToggle import ModeToggle
from AutoToggle import AutoToggle
from switch_button import SwitchButton
from traffic_light_buttons import TrafficLightButton
from crossing_button import CrossingButton
from block_occupancy import BlockOccupancy

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

    def create_shared_content(self, editable):
        tab_widget = QWidget()

        # Main layout for the entire tab
        main_layout = QHBoxLayout(tab_widget)

        # Left side layout for Block Occupancy and Dropdown Menu
        left_layout = QVBoxLayout()

        # Create dropdown menu for line selection
        lines_dropdown_menu = QComboBox()
        lines_dropdown_menu.addItems(["Blue", "Green", "Red"])
        lines_dropdown_menu.setFixedHeight(40)  # Adjust height for a consistent look
        left_layout.addWidget(lines_dropdown_menu)

        # Add label for Block Occupancy
        left_layout.addWidget(QLabel("Block Occupancy"))

        # Create scroll area for block occupancy (left side)
        block_scroll = QScrollArea()
        block_scroll_widget = QWidget()
        block_layout = QVBoxLayout(block_scroll_widget)
        block_layout.setSpacing(10)  # Ensure consistent spacing for checkboxes
        block_scroll.setWidget(block_scroll_widget)
        block_scroll.setWidgetResizable(True)
        left_layout.addWidget(block_scroll)

        # Right side layout for buttons (traffic lights, switches, crossings)
        right_layout = QVBoxLayout()

        # Add HW/SW toggle button
        hw_sw_toggle_button = QPushButton("Hardware")
        right_layout.addWidget(hw_sw_toggle_button)

        # Add Manual/Auto toggle button
        manual_auto_toggle_button = QPushButton("Auto")
        right_layout.addWidget(manual_auto_toggle_button)

        # Add label for Traffic Lights
        right_layout.addWidget(QLabel("Traffic Lights"))

        # Scroll area for traffic lights (right side)
        traffic_lights_scroll = QScrollArea()
        traffic_lights_widget = QWidget()
        traffic_lights_layout = QVBoxLayout(traffic_lights_widget)
        traffic_lights_layout.setSpacing(10)  # Ensure consistent spacing for traffic light buttons
        traffic_lights_scroll.setWidget(traffic_lights_widget)
        traffic_lights_scroll.setWidgetResizable(True)
        right_layout.addWidget(traffic_lights_scroll)

        # Add label for Switches
        right_layout.addWidget(QLabel("Switches"))

        # Scroll area for switches (right side)
        switches_scroll = QScrollArea()
        switches_widget = QWidget()
        switches_layout = QVBoxLayout(switches_widget)
        switches_layout.setSpacing(10)  # Ensure consistent spacing for switches
        switches_scroll.setWidget(switches_widget)
        switches_scroll.setWidgetResizable(True)
        right_layout.addWidget(switches_scroll)

        # Add label for Crossings
        right_layout.addWidget(QLabel("Crossings"))

        # Scroll area for crossings (right side)
        crossings_scroll = QScrollArea()
        crossings_widget = QWidget()
        crossings_layout = QVBoxLayout(crossings_widget)
        crossings_layout.setSpacing(10)  # Ensure consistent spacing for crossings
        crossings_scroll.setWidget(crossings_widget)
        crossings_scroll.setWidgetResizable(True)
        right_layout.addWidget(crossings_scroll)

        # Function to update content when switching lines
        def update_content():
            self.line = lines_dropdown_menu.currentText()

            # Clear the current content in all scroll areas
            clear_layout(block_layout)
            clear_layout(traffic_lights_layout)
            clear_layout(switches_layout)
            clear_layout(crossings_layout)

            # Check if the selected line exists in the data
            if self.line in data:
                # Check the mode (HW/SW) and make sure the mode exists in the JSON
                if self.mode in data[self.line]:
                    mode_data = data[self.line][self.mode]

                    # Add blocks (if any)
                    if 'blocks' in mode_data and mode_data['blocks']:
                        for block in mode_data['blocks']:
                            block_checkbox = QCheckBox(f"Block {block['block']}")
                            block_checkbox.setChecked(block['occupied'])
                            block_checkbox.setFixedHeight(40)  # Ensure consistent height for block checkboxes
                            block_layout.addWidget(block_checkbox)

                    # Add traffic lights (if any)
                    if 'traffic_lights' in mode_data and mode_data['traffic_lights']:
                        for light in mode_data['traffic_lights']:
                            traffic_light_button = TrafficLightButton(
                                name_1=light['name_1'],
                                name_2=light['name_2']
                            )
                            traffic_light_button.setFixedHeight(40)  # Ensure consistent height for traffic light buttons
                            traffic_lights_layout.addWidget(traffic_light_button)

                    # Add switches (if any)
                    if 'switches' in mode_data and mode_data['switches']:
                        for switch in mode_data['switches']:
                            switch_button = SwitchButton(
                                name_1=switch['name_1'],
                                name_2=switch['name_2']
                            )
                            switch_button.setFixedHeight(40)  # Ensure consistent height for switch buttons
                            switches_layout.addWidget(switch_button)

                    # Add crossings (if any)
                    if 'crossings' in mode_data and mode_data['crossings']:
                        for crossing in mode_data['crossings']:
                            crossing_button = CrossingButton(
                                name_1=crossing['name_1'],
                                name_2=crossing['name_2']
                            )
                            crossing_button.setFixedHeight(40)  # Ensure consistent height for crossing buttons
                            crossings_layout.addWidget(crossing_button)

                # Set updated widgets and layouts
                block_scroll.setWidget(block_scroll_widget)
                traffic_lights_scroll.setWidget(traffic_lights_widget)
                switches_scroll.setWidget(switches_widget)
                crossings_scroll.setWidget(crossings_widget)

        # Function to clear layouts
        def clear_layout(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Connect dropdown menu to update content function
        lines_dropdown_menu.currentIndexChanged.connect(update_content)

        # Toggle between Hardware and Software modes
        def toggle_hw_sw_mode():
            if self.mode == "HW":
                self.mode = "SW"
                hw_sw_toggle_button.setText("Software")  # Change text to "Software"
            else:
                self.mode = "HW"
                hw_sw_toggle_button.setText("Hardware")  # Change text to "Hardware"
            update_content()

        hw_sw_toggle_button.clicked.connect(toggle_hw_sw_mode)

        # Toggle between Manual and Auto modes
        def toggle_manual_auto_mode():
            if manual_auto_toggle_button.text() == "Auto":
                manual_auto_toggle_button.setText("Manual")
                # Add additional logic for switching to Manual mode here
            else:
                manual_auto_toggle_button.setText("Auto")
                # Add additional logic for switching to Auto mode here

        manual_auto_toggle_button.clicked.connect(toggle_manual_auto_mode)

        # Initial content load
        update_content()

        # Add left and right layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        return tab_widget

    def create_main_tab(self):
        self.main_tab = self.create_shared_content(editable=False)
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
        test_content = self.create_shared_content(editable=True)
        test_layout.addWidget(test_content)

        self.tabs.addTab(self.test_tab, "Test")



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



