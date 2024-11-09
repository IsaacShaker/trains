import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100, 100, 850, 550)
        self.setStyleSheet("background-color: grey")
        
        # Initialize variables to store input
        self.input_value1 = ""
        self.input_value2 = ""

        # Create a font for labels and inputs
        big_font = QFont("Arial", 14)

        # Create labels
        self.label1 = QLabel("Red Track Excel Data", self)
        self.label1.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label1.setFont(big_font)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label1.setGeometry(165, 100, 210, 40)  # Position: (x=100, y=50), Size: (width=210, height=30)

        self.label2 = QLabel("Green Track Excel Data", self)
        self.label2.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label2.setFont(big_font)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label2.setGeometry(475, 100, 210, 40)  # Position: (x=400, y=50), Size: (width=210, height=30)

        # First text entry with custom position and size
        self.text_entry1 = QLineEdit(self)
        self.text_entry1.setFont(big_font)
        self.text_entry1.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry1.setPlaceholderText("Enter first value")
        self.text_entry1.setText("trackData/RedLine.xlsx")
        self.text_entry1.setGeometry(150, 150, 240, 40)  # Position: (x=100, y=100), Size: (width=230, height=40)

        # Second text entry with custom position and size
        self.text_entry2 = QLineEdit(self)
        self.text_entry2.setFont(big_font)
        self.text_entry2.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry2.setPlaceholderText("Enter second value")
        self.text_entry2.setText("trackData/GreenLine.xlsx")
        self.text_entry2.setGeometry(460, 150, 240, 40)  # Position: (x=400, y=100), Size: (width=230, height=40)

        # Save button with custom position and size
        self.button = QPushButton("Build Track", self)
        self.button.setStyleSheet("background-color: #772CE8; color: black")
        self.button.setFont(big_font)
        self.button.setGeometry(365, 240, 120, 50)  # Position: (x=325, y=200), Size: (width=120, height=50)
        self.button.clicked.connect(self.save_text)

    def save_text(self):
        # Store text entry values in separate variables
        self.input_value1 = self.text_entry1.text()
        self.input_value2 = self.text_entry2.text()
        print("Text 1 saved:", self.input_value1)
        print("Text 2 saved:", self.input_value2)

# Main entry to start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
