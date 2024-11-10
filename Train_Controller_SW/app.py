import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# Function to be executed when the button is clicked
def on_button_click():
    print("Button clicked!")

# The main function
def main():
    # Create the main application
    app = QApplication(sys.argv)

    # Create a window
    window = QWidget()

    window.setWindowTitle('Basic PyQt Button Example')

    # Create a button and connect it to the function
    button = QPushButton('Click Me')
    button.clicked.connect(on_button_click)

    # Set up layout
    layout = QVBoxLayout()
    layout.addWidget(button)

    # Set the layout to the window
    window.setLayout(layout)

    # Show the window
    window.show()

    # Run the application loop
    sys.exit(app.exec())

# Standard Python convention for running the script
if __name__ == '__main__':
    main()
