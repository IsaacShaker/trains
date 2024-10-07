from PyQt6.QtWidgets import QPushButton

class ModeToggle(QPushButton):
    def __init__(self, initial_mode, callback):
        super().__init__('Software Mode' if initial_mode == 'SW' else 'Hardware Mode')
        self.mode = initial_mode
        self.clicked.connect(lambda: self.toggle_mode(callback))

    def toggle_mode(self, callback):
        if self.mode == 'HW':
            self.setText('Software Mode')
            self.mode = 'SW'
        else:
            self.setText('Hardware Mode')
            self.mode = 'HW'
        callback(self.mode)
