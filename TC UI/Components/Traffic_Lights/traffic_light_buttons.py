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
        print("Sending Traffic Light States to CTC and Track Model ...")
        self.set_light()

    def set_editable(self, editable):
        self.setEnabled(editable)  # Enable or disable the button based on mode

