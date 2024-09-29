import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("CTC Office")

        # Set a fixed size for the window
        self.setFixedSize(800, 850)  # Width: 800, Height: 850

        # Set the background color of the window using a color code
        self.setStyleSheet("background-color: #FFFFFF;")  # Light blue background

        # Create the tab widget and set it as the central widget of the window
        self.tab_widget = QTabWidget()
        # Style the tab buttons
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #171717;    /* Background color of the tab */
                color: white;           /* Text color */
                padding: 10px;          /* Padding inside the tab */
                border: 1px solid #FFFFFF; /* Border around the tab */
                border-bottom: none;    /* No border at the bottom */
            }
            QTabBar::tab:selected {
                background: #772CE8;    /* Background color for the selected tab */
                color: white;           /* Text color of the selected tab */
            }
        """)
        self.setCentralWidget(self.tab_widget)
        # Add tabs to the tab widget
        self.create_tabs()

    def create_tabs(self):
        # Create the first tab content
        home = QWidget()
        home_layout = QVBoxLayout()
        home_label = QLabel("This is Tab 1")
        home_layout.addWidget(home_label)
        home.setLayout(home_layout)
        home.setStyleSheet("background-color: #171717;")  # Black background

        # Create the second tab content
        testBench = QWidget()
        testBench_layout = QVBoxLayout()
        testBench_label = QLabel("This is Tab 2")
        testBench_layout.addWidget(testBench_label)
        testBench.setLayout(testBench_layout)
        testBench.setStyleSheet("background-color: #171717;")  # Alice blue background

        # Add the tabs to the tab widget
        self.tab_widget.addTab(home, "Home")
        self.tab_widget.addTab(testBench, "Test Bench")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()

    sys.exit(app.exec())
