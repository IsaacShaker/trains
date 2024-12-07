from PyQt6.QtWidgets import QPushButton

class AutoToggle(QPushButton):
    def __init__(self, is_auto):
        super().__init__()
        self.setLabel(is_auto)

    def refresh(self, is_auto):
        self.setLabel(is_auto)
    
    def setLabel(self, is_auto):
        if is_auto:
            self.setText("Auto")
        else:
            self.setText("Manual")