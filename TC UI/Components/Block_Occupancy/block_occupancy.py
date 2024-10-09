import os
import sys
from PyQt6.QtWidgets import QCheckBox, QVBoxLayout, QWidget

class BlockOccupancy(QWidget):
    def __init__(self, data, line, mode, editable=False):
        super().__init__()
        self.line = line
        self.mode = mode
        self.track_data = data
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Refresh the checkboxes based on the line and mode
        self.refresh(line, mode, editable)

    def refresh(self, line, mode, editable):
        self.clear_layout()
        self.line = line
        self.mode = mode

        # Create checkboxes dynamically based on JSON data
        self.checkboxes = []
        i = 0
        for block in self.track_data[self.line][self.mode]["blocks"]:  # Ensure we always create 15 checkboxes
            checkbox = QCheckBox(f'Block: {block["block"]}')
            checkbox.setChecked(block["occupied"])
            
            # Store the index (or ID) of the block in the checkbox object
            checkbox.block_index = i
            i += 1

            # Connect to a modified state change handler that uses the ID
            checkbox.stateChanged.connect(self.on_state_change)

            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.set_checkbox_interaction(editable)

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

    def set_checkbox_interaction(self, editable):
        """Enable or disable checkboxes based on the 'editable' flag."""
        for checkbox in self.checkboxes:
            checkbox.setEnabled(editable)



