import os
import sys
from PyQt6.QtWidgets import QCheckBox, QVBoxLayout, QWidget
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json')))
from json_helpers import load_json, save_json


class BlockOccupancy(QWidget):
    def __init__(self, line, mode):
        super().__init__()
        self.line = line
        self.mode = mode
        self.track_data = {}
        self.layout = QVBoxLayout(self)

        self.refresh(line, mode)

    def refresh(self, line, mode):
        self.clear_layout()
        self.line = line
        self.mode = mode
        self.track_data = load_json()

        # Create checkboxes dynamically based on JSON data
        self.checkboxes = []
        for i, block in enumerate(self.track_data[self.line][self.mode]["blocks"]):
            checkbox = QCheckBox(f'Block: {block["block"]}')
            checkbox.setChecked(block["occupied"])
            
            # Store the index (or ID) of the block in the checkbox object
            checkbox.block_index = i

            # Connect to a modified state change handler that uses the ID
            checkbox.stateChanged.connect(self.on_state_change)

            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)


    def clear_layout(self):
        # Remove and delete all items from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)  # Take the first item
            widget = item.widget()  # Get the widget
            if widget is not None:
                widget.deleteLater()  # Safely delete the widget


    def on_state_change(self):
        """Saves the new state of the checkbox when the user interacts with the checkboxes"""
        # Get the sender (the checkbox that triggered the state change)
        checkbox = self.sender()

        # Access the corresponding block directly using the index stored in the checkbox
        block_index = checkbox.block_index
        self.track_data[self.line][self.mode]["blocks"][block_index]["occupied"] = checkbox.isChecked()

        # Save the updated state to the JSON file
        save_json(self.track_data)
    

    def set_checkbox_interaction(self, editable):
        """Enable or disable checkboxes based on the 'editable' flag."""
        for checkbox in self.checkboxes:
            checkbox.setEnabled(editable)