import sys
import os


from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QSizePolicy
)

from TrainModel_UI import Train_UI
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtCore import Qt

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        #Initialize UI and show it
        self.train_model=Train_UI()
        self.train_model.show()

        #Enter test values
        self.train_model.train_list[0].set_commanded_power(120000)

if __name__ == "__main__":    
    app = MainApp(sys.argv)
    sys.exit(app.exec())