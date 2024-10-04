from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QStackedWidget, QVBoxLayout, QLabel
import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set a fixed window size
        self.setFixedSize(725, 525)
        self.setWindowTitle("Train Controller Software - Micah Smith")

        # Create the QStackedWidget to hold both screens (Main Control and Test Bench)
        self.stacked_widget = QStackedWidget()

        # Create main control screen widget
        self.main_control_widget = QWidget()
        self.setup_main_control_layout()

        # Create test bench screen widget
        self.test_bench_widget = QWidget()
        self.setup_test_bench_layout()

        # Add both widgets to the stacked widget
        self.stacked_widget.addWidget(self.main_control_widget)
        self.stacked_widget.addWidget(self.test_bench_widget)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stacked_widget)

    def setup_main_control_layout(self):
        layout = QVBoxLayout(self.main_control_widget)

        # A shared widget that will be used in both screens
        self.shared_label = QLabel("Shared Label in both screens")
        layout.addWidget(self.shared_label)

        # Button to switch to Test Bench screen
        self.switch_to_test_bench_button = QPushButton("Switch to Test Bench", self.main_control_widget)
        layout.addWidget(self.switch_to_test_bench_button)
        self.switch_to_test_bench_button.clicked.connect(self.show_test_bench)

    def setup_test_bench_layout(self):
        layout = QVBoxLayout(self.test_bench_widget)

        # The same shared widget (referenced in both screens)
        layout.addWidget(self.shared_label)

        # Button to switch back to Main Control screen
        self.switch_to_main_control_button = QPushButton("Switch to Main Control", self.test_bench_widget)
        layout.addWidget(self.switch_to_main_control_button)
        self.switch_to_main_control_button.clicked.connect(self.show_main_control)

    def show_test_bench(self):
        # Switch to the Test Bench screen (index 1)
        self.stacked_widget.setCurrentIndex(1)

    def show_main_control(self):
        # Switch back to the Main Control screen (index 0)
        self.stacked_widget.setCurrentIndex(0)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
