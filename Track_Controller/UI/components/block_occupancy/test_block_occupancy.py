# test_block_occupancy.py
import sys
import unittest
import argparse
from PyQt6.QtWidgets import QApplication, QMainWindow
from block_occupancy import BlockOccupancy

# For Standalone Testing
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the block occupancy component
        self.block_occupancy_widget = BlockOccupancy("Blue", "HW")
        self.setCentralWidget(self.block_occupancy_widget)


# Unit Test Section
class TestBlockOccupancy(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])  # PyQt application for testing
        self.block_occupancy = BlockOccupancy()

    def test_initial_checkbox_state(self):
        block_data = self.block_occupancy.blocks_data
        for i, checkbox in enumerate(self.block_occupancy.checkboxes):
            self.assertEqual(checkbox.isChecked(), block_data[i]["occupied"])

    def test_checkbox_toggle(self):
        checkbox = self.block_occupancy.checkboxes[0]
        initial_state = checkbox.isChecked()
        checkbox.toggle()
        self.assertEqual(self.block_occupancy.blocks_data[0]["occupied"], not initial_state)

    def tearDown(self):
        self.app.quit()


def run_standalone():
    """Runs the standalone PyQt application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def run_tests():
    """Runs the unit tests."""
    unittest.main(argv=[''], exit=False)


if __name__ == "__main__":
    # Argument parsing to switch between standalone and unittest modes
    parser = argparse.ArgumentParser(description="Switch between standalone and unittest modes.")
    parser.add_argument('--test', action='store_true', help="Run unit tests.")
    args = parser.parse_args()

    if args.test:
        run_tests()
    else:
        run_standalone()
