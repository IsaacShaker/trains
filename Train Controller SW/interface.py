from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

app = QApplication([])

# Create a main window
window = QWidget()
layout = QVBoxLayout()

# Create a QLabel with HTML styling
label = QLabel()
label.setText('<span style="color: red;">Red Text</span> and <span style="color: blue;">Blue Text</span>')
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

layout.addWidget(label)
window.setLayout(layout)

# Show the window
window.show()

app.exec()
