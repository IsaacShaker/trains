from PyQt6.QtWidgets import QVBoxLayout, QWidget
from Components.Switches.switch_button import SwitchButton

class Switches(QWidget):
    def __init__(self, data, line, mode, editable=False):
        super().__init__()
        self.line = line
        self.mode = mode
        self.track_data = data
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Refresh the checkboxes based on the line and mode
        self.refresh(line, mode, editable)

    def refresh(self, line, mode, editable=False):
        self.clear_layout()
        self.line = line
        self.mode = mode

        # Create checkboxes dynamically based on JSON data
        for switch in self.track_data[self.line][self.mode]['switches']:
            switch_button = SwitchButton(switch, editable)
            switch_button.setFixedHeight(40)  # Ensure consistent height for traffic light buttons
            self.layout.addWidget(switch_button)

    def clear_layout(self):
        # Remove and delete all items from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)  # Take the first item
            widget = item.widget()  # Get the widget
            if widget is not None:
                widget.deleteLater()  # Safely delete the widget



