from PyQt6.QtWidgets import QPushButton

class AutoToggle(QPushButton):
    def __init__(self, is_auto, callback):
        super().__init__('Auto Mode' if is_auto else 'Manual Mode')
        self.is_auto = is_auto
        self.clicked.connect(lambda: self.toggle_auto(callback))

    def toggle_auto(self, callback):
        if self.is_auto:
            self.setText('Manual Mode')
            self.is_auto = False
        else:
            self.setText('Auto Mode')
            self.is_auto = True
        callback(self.is_auto)
