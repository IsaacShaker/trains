from PyQt6.QtWidgets import QPushButton

class CrossingButton(QPushButton):
    def __init__(self, name_1, name_2, toggled=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setObjectName("crossingButton")  # Set the object name for QSS

        self.name_1 = name_1
        self.name_2 = name_2
        self.toggled = toggled

        # Set the initial button label
        self.setText(self.get_label())

        # Connect button press to toggle function
        self.clicked.connect(self.toggle_crossing)

    def toggle_crossing(self):
        self.toggled = not self.toggled
        self.setText(self.get_label())
        self.update_style()

    def update_style(self):
        if self.toggled:
            self.setStyleSheet("background-color: yellow; color: black;")  # Set yellow background for active
        else:
            self.setStyleSheet("background-color: purple; color: black;")  # Set purple background for inactive

    def get_label(self):
        return self.name_2 if self.toggled else self.name_1
