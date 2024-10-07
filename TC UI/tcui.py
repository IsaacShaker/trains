import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTabWidget, QComboBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Get the screen geometry
        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # Set window geometry to occupy the left half of the screen
        self.setWindowTitle('My PyQt App')
        self.setGeometry(0, 0, self.screen_width // 2, self.screen_height)
        
        # Create a QTabWidget that fills the whole window
        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(0, 0, self.screen_width // 2, self.screen_height)
        
        # Initialize tabs
        self.create_main_tab()
        self.create_test_tab()
        self.create_upload_tab()

    def toggle_button(self, button):
        if button.text() == "Hardware Mode":
            button.setText("Software Mode")
        else:
            button.setText("Hardware Mode")

    def toggle_button_2(self, button):
        if button.text() == "Auto Mode":
            button.setText("Manual Mode")
        else:
            button.setText("Auto Mode")

    def create_main_tab(self):
        self.main_tab = QWidget()
        self.tabs.addTab(self.main_tab, "Main")
        
        # Create dropdown menu and set its geometry
        self.dropdown_menu = QComboBox(self.main_tab)
        self.dropdown_menu.addItems(["Blue Line", "Green Line", "Red Line"])
        self.dropdown_menu.setGeometry(25, 25, 150, 45)  # Adjusted dropdown size
        
        # Create buttons and set their geometry directly
        self.main_button_1 = QPushButton('Hardware Mode', self.main_tab)
        self.main_button_2 = QPushButton('Auto Mode', self.main_tab)
        self.main_button_1.setGeometry(475, 25, 150, 45)  # Adjusted button size
        self.main_button_2.setGeometry(325, 25, 150, 45)  # Adjusted button size
        self.main_button_1.clicked.connect(lambda: self.toggle_button(self.main_button_1))
        self.main_button_2.clicked.connect(lambda: self.toggle_button_2(self.main_button_2))

    def create_test_tab(self):
        self.test_tab = QWidget()
        self.tabs.addTab(self.test_tab, "Test")
        
        # Create dropdown menu and set its geometry
        self.dropdown_menu_test = QComboBox(self.test_tab)
        self.dropdown_menu_test.addItems(["Blue Line", "Green Line", "Red Line"])
        self.dropdown_menu_test.setGeometry(25, 25, 150, 45)  # Adjusted dropdown size
        
        # Create buttons and set their geometry directly
        self.test_button_1 = QPushButton('Hardware Mode', self.test_tab)
        self.test_button_2 = QPushButton('Auto Mode', self.test_tab)
        self.test_button_1.setGeometry(475, 25, 150, 45)  # Adjusted button size
        self.test_button_2.setGeometry(325, 25, 150, 45)  # Adjusted button size
        self.test_button_1.clicked.connect(lambda: self.toggle_button(self.test_button_1))
        self.test_button_2.clicked.connect(lambda: self.toggle_button_2(self.test_button_2))

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
        from PyQt6.QtWidgets import QFileDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PLC Files (*.plc)")
        file_dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()  # Show the window occupying the left half of the screen
    sys.exit(app.exec())
