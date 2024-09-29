import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

# Function to handle button click
def on_button_click():
    label.setText("Button Clicked!")

# Create the application
app = QApplication(sys.argv)

# Create a main window
window = QWidget()
window.setWindowTitle("My PyQt6 UI")
window.setGeometry(100, 100, 300, 200)  # x, y, width, height

# Create a vertical layout
layout = QVBoxLayout()

# Create a label
label = QLabel("Hello, World!")
layout.addWidget(label)

# Create a button
button = QPushButton("Click Me")
button.clicked.connect(on_button_click)  # Connect button click to the function
layout.addWidget(button)

# Set the layout to the window
window.setLayout(layout)

# Show the window
window.show()

# Start the application
sys.exit(app.exec())