from PyQt6.QtWidgets import QPushButton

class ModeToggle(QPushButton):
    def __init__(self, mode):
        super().__init__()
        self.setLabel(mode)

    def refresh(self, mode):
        self.setLabel(mode)
    
    def setLabel(self, mode):
        if mode == "SW":
            self.setText("Software")
        else:
            self.setText("Hardware")