# traffic_light_buttons.py

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

class TrafficLightButton(QPushButton):
    def __init__(self, name_1, name_2, parent=None):
        super().__init__(parent)
        self.name_1 = name_1
        self.name_2 = name_2
        
        # Set the initial text to name_1
        self.setText(self.name_1)
        self.setStyleSheet("background-color: red;")  # Default color

        # Signal connection for button click
        self.clicked.connect(self.toggle_light)

    def toggle_light(self):
        if not self.isEnabled():  # Only toggle if enabled
            return
        # Toggle between name_1 and name_2
        current_text = self.text()
        new_text = self.name_2 if current_text == self.name_1 else self.name_1
        self.setText(new_text)
        
        # Update color based on the current state
        if self.styleSheet() == "background-color: red;":
            self.setStyleSheet("background-color: green;")  # Active state
        else:
            self.setStyleSheet("background-color: red;")  # Inactive state

    def set_editable(self, editable):
        self.setEnabled(editable)  # Enable or disable the button based on mode

    def get_state(self):
        """Return the current state of the button as a dictionary."""
        return {
            'text': self.text(),
            'color': self.styleSheet()  # You can also store color if needed
        }

    def set_state(self, state):
        """Set the state of the button based on the provided state dictionary."""
        self.setText(state['text'])
        self.setStyleSheet(state['color'])  # Restore the color

