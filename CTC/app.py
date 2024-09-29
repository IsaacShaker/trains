import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("CTC Office")

        # Set a fixed size for the window
        self.setFixedSize(800, 875)  # Width: 800, Height: 850

        # Set the background color of the window using a color code
        self.setStyleSheet("background-color: #171717;")  # Dark background

        # Create the tab widget and set it as the central widget of the window
        self.tab_widget = QTabWidget()

        # Style the tab buttons
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #171717;  /* Tab button background color */
                color: white;         /* Tab button text color */
                padding: 10px;        /* Padding inside the tab */
                border: 1px solid #FFFFFF; /* Border color */
                border-bottom: none;  /* No border at the bottom */
            }
            QTabBar::tab:selected {
                background: #772CE8;  /* Background color for the selected tab */
                color: white;         /* Text color of the selected tab */
            }
        """)

        self.setCentralWidget(self.tab_widget)

        # Add the tabs to the tab widget
        self.create_tabs()

    def create_tabs(self):
        # Home Tab content
        home = QWidget()
        home_layout = QVBoxLayout()

        # Call the layout with frames to organize the UI for Home tab
        self.create_home_layout(home_layout)

        home.setLayout(home_layout)
        home.setStyleSheet("background-color: #171717;")  # Black background

        # Test Bench Tab content
        test_bench = QWidget()
        test_bench_layout = QVBoxLayout()

        # Add a placeholder for Test Bench, feel free to customize later
        test_bench_label = QLabel("Test Bench content goes here.")
        test_bench_label.setStyleSheet("color: white; font-size: 18px;")
        test_bench_layout.addWidget(test_bench_label)

        test_bench.setLayout(test_bench_layout)
        test_bench.setStyleSheet("background-color: #171717;")  # Black background

        # Add the tabs to the tab widget
        self.tab_widget.addTab(home, "Home")
        self.tab_widget.addTab(test_bench, "Test Bench")

    def create_home_layout(self, layout):
        # Main layout grid for Home tab
        grid_layout = QGridLayout()

        # Add the sections like in the provided image

        # 1. Maintenance Section (Top left)
        maintenance_frame = self.create_section_frame()
        maintenance_layout = QVBoxLayout()
        maintenance_label = QLabel("Maintenance")
        maintenance_label.setStyleSheet("color: white; font-size: 18px;")
        maintenance_layout.addWidget(maintenance_label)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: yellow; color: black;")
        reopen_button = QPushButton("Reopen")
        reopen_button.setStyleSheet("background-color: green; color: white;")

        maintenance_layout.addWidget(close_button)
        maintenance_layout.addWidget(reopen_button)
        maintenance_frame.setLayout(maintenance_layout)
        grid_layout.addWidget(maintenance_frame, 0, 0)

        # 2. Simulation Speed Section (Top right)
        speed_frame = self.create_section_frame()
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Simulation Speed")
        speed_label.setStyleSheet("color: white; font-size: 18px;")
        speed_layout.addWidget(speed_label)

        # Add widgets for simulation speed (placeholders)
        speed_layout.addWidget(QLabel("Speed controls go here"))
        speed_frame.setLayout(speed_layout)
        grid_layout.addWidget(speed_frame, 0, 1)

        # 3. Schedule Builder Section (Middle)
        schedule_frame = self.create_section_frame()
        schedule_layout = QVBoxLayout()
        schedule_label = QLabel("Schedule Builder")
        schedule_label.setStyleSheet("color: white; font-size: 18px;")
        schedule_layout.addWidget(schedule_label)

        # Add widgets for schedule builder (placeholders)
        schedule_layout.addWidget(QLabel("Auto/Manual Toggle goes here"))
        schedule_frame.setLayout(schedule_layout)
        grid_layout.addWidget(schedule_frame, 1, 0, 1, 2)  # Span two columns

        # 4. Dispatch Rate Section (Lower left)
        dispatch_frame = self.create_section_frame()
        dispatch_layout = QVBoxLayout()
        dispatch_label = QLabel("Dispatch Rate")
        dispatch_label.setStyleSheet("color: white; font-size: 18px;")
        dispatch_layout.addWidget(dispatch_label)

        # Add widgets for dispatch rate (placeholders)
        dispatch_layout.addWidget(QLabel("4 Trains/hr display goes here"))
        dispatch_frame.setLayout(dispatch_layout)
        grid_layout.addWidget(dispatch_frame, 2, 0)

        # 5. Train Data Section (Lower right)
        train_frame = self.create_section_frame()
        train_layout = QVBoxLayout()
        train_label = QLabel("Train Data")
        train_label.setStyleSheet("color: white; font-size: 18px;")
        train_layout.addWidget(train_label)

        # Add widgets for train data (placeholders)
        train_layout.addWidget(QLabel("Train data display goes here"))
        train_frame.setLayout(train_layout)
        grid_layout.addWidget(train_frame, 2, 1)

        # 6. Block Occupancies (Bottom)
        blocks_frame = self.create_section_frame()
        blocks_layout = QVBoxLayout()
        blocks_label = QLabel("Block Occupancies")
        blocks_label.setStyleSheet("color: white; font-size: 18px;")
        blocks_layout.addWidget(blocks_label)

        # Add widgets for train data (placeholders)
        blocks_layout.addWidget(QLabel("Block occupancies go here"))
        blocks_frame.setLayout(blocks_layout)
        grid_layout.addWidget(blocks_frame, 2, 1)

        layout.addLayout(grid_layout)

    def create_section_frame(self):
        """Helper function to create a QFrame with consistent styling."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Sunken)
        frame.setStyleSheet("border: 2px solid white;")
        return frame


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MyWindow()
    window.show()

    sys.exit(app.exec())
