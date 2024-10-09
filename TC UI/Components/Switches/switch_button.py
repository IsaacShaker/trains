from PyQt6.QtWidgets import QPushButton

class SwitchButton(QPushButton):
    def __init__(self, data, editable=False):
        super().__init__()
        self.data = data
        
        # Set the initial text and style
        self.set_crossing()

        # Set edit permissions
        self.set_editable(editable)
        
        # Signal connection for button click
        self.clicked.connect(self.toggle_crossing)

    def toggle_crossing(self):
        if self.data["toggled"] == True:
            self.data["toggled"] = False
        else:
            self.data["toggled"] = True
        
        self.set_crossing()

    def set_crossing(self):
        new_text = self.data["name_2"] if self.data["toggled"] else self.data["name_1"]
        self.setText(new_text)

        # new_style = "background-color: yellow; color: black;" if self.data["toggled"] else "background-color: purple; color: black;"
        # self.setStyleSheet(new_style)  # Set yellow background for active

    def set_editable(self, editable):
        self.setEnabled(editable)  # Enable or disable the button based on mode
