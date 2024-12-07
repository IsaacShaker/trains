import sys
from CTC.ctc import MyWindow
from PyQt6.QtWidgets import QApplication, QDialog

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.ctc = MyWindow()
        self.ctc.show()

        self.ctc.submit_dispatch('Green', 'New Train', 'PIONEER', '10:00:00')

if __name__ == '__main__':
    ex = MainApp(sys.argv)
    # Start the API server and pass the MyApp instance
    sys.exit(ex.exec())