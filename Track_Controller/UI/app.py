import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTabWidget, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt6.QtCore import QFile, QTextStream, QIODevice
from components.block_occupancy.block_occupancy import BlockOccupancy

lines = ["Blue", "Green", "Red"]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initial properties of the UI
        self.line = "Blue"
        self.mode = "SW"
        self.auto = True
        self.updating_tab = False

        # Get the screen geometry
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Set window geometry to occupy the left half of the screen
        self.setWindowTitle('Track Controller UI')
        self.setGeometry(0, 0, self.screen_width // 2, self.screen_height)
        
        # self.load_stylesheet("styles.qss")

        # Create a QTabWidget that fills the whole window
        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, self.screen_width // 2, self.screen_height)

        # Initialize tabs
        self.create_main_tab()
        self.create_test_tab()
        self.create_upload_tab()
        self.tabs.currentChanged.connect(self.rerender_tab)


    def load_stylesheet(self, file_name):
        """Load a stylesheet from a file."""
        file = QFile(file_name)
        if file.open(QIODevice.OpenModeFlag.ReadOnly):  # Use QIODevice.OpenModeFlag.ReadOnly
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print(f"Error: Unable to open stylesheet file '{file_name}'")


    def toggle_mode(self, button):
        # change button text and wayside controller mode
        if self.mode == "HW":
            button.setText("Software Mode")
            self.mode = "SW"
        else:
            button.setText("Hardware Mode")
            self.mode = "HW"

        current_tab_index = self.tabs.currentIndex()
        self.rerender_tab(current_tab_index)


    def toggle_auto(self, button):
        # change button text and wayside controller auto
        if self.auto == True:
            button.setText("Manual Mode")
            self.auto = False
        else:
            button.setText("Auto Mode")
            self.auto = True
        
        current_tab_index = self.tabs.currentIndex()
        self.rerender_tab(current_tab_index)
    
    def rerender_tab(self, index):
        # NOTE: this function causes the main tab to render twice in the begining, try to solve this bug
        """Refresh all components in the Main tab when switching to it."""
        # Rerenders the block occupancy section
        if self.tabs.tabText(index) == "Main":
            block_occupancy = self.main_tab.findChild(BlockOccupancy)
            if block_occupancy:
                block_occupancy.refresh(self.line, self.mode)
                block_occupancy.set_checkbox_interaction(False) # Disable the checkboxes


        # NOTE: Experimental and not working properly, intended to be able to rerender the entire tab
        # if index >= 0 and self.updating_tab == False:
        #     # Set the flag to indicate that we're updating the tab
        #     self.updating_tab = True
        #     tab_text = self.tabs.tabText(index)
        #     # Remove the tab at the current index
        #     self.tabs.removeTab(index)

        #     # Create new content for the tab
        #     new_tab = self.create_shared_content(editable=False)

        #     # Insert the new tab at the same index with the same label "Main"
        #     self.tabs.insertTab(index, new_tab, tab_text)

        #     # Reset the flag after updating the tab
        #     self.updating_tab = False


    def create_shared_content(self, editable):
        """
        Create the shared content for both the test and main tabs.
        :param editable: Boolean, if True checkboxes are editable, otherwise they are read-only.
        """
        # Create a widget for the tab content
        tab_widget = QWidget()

        # Create a vertical layout for the tab content
        main_layout = QVBoxLayout(tab_widget)

        # Create a horizontal layout for the dropdown and buttons
        horizontal_layout = QHBoxLayout()

        # Create dropdown menu and add it to the horizontal layout
        lines_dropdown_menu = QComboBox()
        lines_dropdown_menu.addItems(lines)
        lines_dropdown_menu.setFixedSize(150, 50)  # Set fixed width and height
        horizontal_layout.addWidget(lines_dropdown_menu)  # Add dropdown to horizontal layout

        # Create buttons and add them to the horizontal layout
        mode_text = 'Hardware Mode' if self.mode == "HW" else 'Software Mode'
        auto_text = 'Auto Mode' if self.auto == True else 'Manual Mode'
        mode_button = QPushButton(mode_text)
        auto_button = QPushButton(auto_text)

        # Set fixed size or minimum size for buttons
        mode_button.setFixedSize(150, 50)  # Set fixed width and height
        auto_button.setFixedSize(150, 50)  # Set fixed width and height

        # Add button click events (you may want to adjust these depending on which tab)
        mode_button.clicked.connect(lambda: self.toggle_mode(mode_button))
        auto_button.clicked.connect(lambda: self.toggle_auto(auto_button))

        horizontal_layout.addWidget(mode_button)  # Add button 1 to horizontal layout
        horizontal_layout.addWidget(auto_button)  # Add button 2 to horizontal layout

        # Add the horizontal layout to the main layout
        main_layout.addLayout(horizontal_layout)

        # Create an instance of BlockOccupancy and add it to the vertical layout
        block_occupancy = BlockOccupancy(self.line, self.mode)
        
        # Enable or disable interaction with checkboxes based on the editable flag
        block_occupancy.set_checkbox_interaction(editable)  # Implement this method inside BlockOccupancy
        
        main_layout.addWidget(block_occupancy)  # Add block occupancy component to the layout

        return tab_widget  # Return the widget with the layout


    def create_test_tab(self):
        """Test tab where the checkboxes are editable."""
        self.test_tab = self.create_shared_content(editable=True)
        self.tabs.addTab(self.test_tab, "Test")


    def create_main_tab(self):
        """Main tab where the checkboxes are not editable."""
        self.main_tab = self.create_shared_content(editable=False)
        self.tabs.addTab(self.main_tab, "Main")


    def create_upload_tab(self):
        self.upload_tab = QWidget()
        self.tabs.addTab(self.upload_tab, "Upload")
        
        # Create button and set its geometry directly
        self.upload_button_1 = QPushButton('Hardware Mode', self.upload_tab)
        self.upload_button_1.setGeometry(475, 25, 150, 45)  # Adjusted button size
        self.upload_button_1.clicked.connect(lambda: self.toggle_button(self.upload_button_1))

        # Create a button with a plus sign to upload a file in the middle of the upload tab
        self.upload_file_button = QPushButton('+', self.upload_tab)
        self.upload_file_button.setGeometry((self.screen_width // 4) - 25, (self.screen_height // 2) - 25, 50, 50)
        self.upload_file_button.clicked.connect(self.open_file_explorer)


    def open_file_explorer(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PLC Files (*.plc)")
        file_dialog.exec()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()  # Show the window occupying the left half of the screen
    sys.exit(app.exec())