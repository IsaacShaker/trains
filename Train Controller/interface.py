import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QPushButton
        self.button = QPushButton("Press Me", self)

        # Apply stylesheet with a checked state
        self.button.setStyleSheet("""
            QPushButton 
            {
                background-color: red;
                color: white;
                border: 3px solid #FF1A1A;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover 
            {
                background-color: #FF6666;  /* button is lighter when hovering */
            }
            QPushButton:pressed 
            {
                background-color: #CC0000;  /* button becomes darker when pressed */
            }
            QPushButton:checked
            {
                background-color: #A56B1A;  /* dark red when checked (stays pressed) */
            }
        """)

        # Make the button checkable (like a toggle button)
        self.button.setCheckable(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

# Application
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
