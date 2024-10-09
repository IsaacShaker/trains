from PyQt6.QtWidgets import QPushButton

class TrafficLightButton(QPushButton):
    def __init__(self, data, editable=False, parent=None):
        super().__init__(parent)
        self.data = data
        
        # Set the initial text and style
        self.set_light()

        # Set edit permissions
        self.set_editable(editable)
        
        # Signal connection for button click
        self.clicked.connect(self.toggle_light)

    def set_light(self):
        if not self.isEnabled():  # Only toggle if enabled
            return
        new_text = self.data["name_1"] if self.data["toggled"] == False else self.data["name_2"]
        self.setText(new_text)
        
        new_style = "background-color: red;" if self.data["toggled"] == False else "background-color: green;"
        self.setStyleSheet(new_style)

    def toggle_light(self):
        if self.data["toggled"] == True:
            self.data["toggled"] = False
        else:
            self.data["toggled"] = True
        
        self.set_light()

    def set_editable(self, editable):
        self.setEnabled(editable)  # Enable or disable the button based on mode

    # def get_state(self):
    #     """Return the current state of the button as a dictionary."""
    #     return {
    #         'text': self.text(),
    #         'color': self.styleSheet()  # You can also store color if needed
    #     }

    # def set_state(self, state):
    #     """Set the state of the button based on the provided state dictionary."""
    #     self.setText(state['text'])
    #     self.setStyleSheet(state['color'])  # Restore the color

