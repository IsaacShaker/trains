from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QDialog, QComboBox, QLineEdit, QFrame
from PyQt6.QtCore import Qt

class MaintenanceSection(QWidget):
    def __init__(self, m_blocks, op_blocks, occ_blocks, parent = None):
        super().__init__(parent)
        self.maintenance_blocks = m_blocks
        self.open_blocks = op_blocks
        self.occupied_blocks = occ_blocks

        # Create Maintenance Section layout
        self.maintenance_frame = parent.create_section_frame(250,80)
        self.layout = QHBoxLayout()
        self.maintenance_label = QLabel("Maintenance")
        self.maintenance_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.maintenance_label.setStyleSheet("color: white; font-size: 20px;")
        self.maintenance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.maintenance_label)

        # Vertical layout for Closure and Opening buttons
        button_layout = QVBoxLayout()

        # Define Maintenance Closure button
        self.closure_button = QPushButton("Closure")
        self.closure_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.closure_button.setStyleSheet("background-color: yellow; color: black;")
        button_layout.addWidget(self.closure_button)

        # Define Maintenance Opening button
        self.opening_button = QPushButton("Opening")
        self.opening_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button_layout.addWidget(self.opening_button)

        # Add the vertical button layout to the main layout
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # Connect button signals if needed
        self.closure_button.clicked.connect(self.closureClicked)

    # Custom dialog for user to select maintenance closure line
    def closureClicked(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Maintenance Report")

        # Apply styles to the dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: #171717;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #772ce8;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #772ce8;
                color: #ffffff;
                selection-background-color: #CCCCFF;
                selection-color: #000000;
            }
            QLineEdit {
                background-color: #772ce8;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #ffffff;
            }
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Create label
        label = QLabel("What Block Requries Maintenance?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QHBoxLayout()

        # Create combo box with options
        combo_box = QComboBox()
        combo_box.addItems(["Blue"])
        h_layout.addWidget(combo_box)

        # Create text entry box
        text_entry = QLineEdit()
        text_entry.setPlaceholderText("1 - 15")
        h_layout.addWidget(text_entry)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_closure(dialog, combo_box.currentText(), text_entry.text()))
        layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_closure(self, dialog, line, block):
        block = int(block)
        self.maintenance_blocks.append((line, block))
        self.maintenance_blocks = sorted(self.maintenance_blocks, key=lambda x: x[1])
        self.update_opening_button_state()
        self.occupied_blocks.append((line, block))
        self.occupied = sorted(self.occupied_blocks, key=lambda x: x[1])
        self.open_blocks.remove((line, block))
        print("Block", block, "on the", line, "line has been closed for maintenance!")
        dialog.accept()

    # The functionality for user opening a block from maintenance
    def openingClicked(self):
        print('in openingClicked')
        dialog = QDialog(self)
        dialog.setWindowTitle("Maintenance Report")

        # Apply styles to the dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: #171717;
            }
            QLabel {
                color: white;
            }
            QComboBox {
                background-color: #772ce8;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #772ce8;
                color: #ffffff;
                selection-background-color: #CCCCFF;
                selection-color: #000000;
            }
            QLineEdit {
                background-color: #772ce8;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #ffffff;
            }
            QPushButton {
                background-color: green;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Create label
        label = QLabel("What Block Needs Opened?")
        layout.addWidget(label)

        # Create horizontal layout for combo box and text entry box
        h_layout = QVBoxLayout()

        # Create combo box with options
        line_combo_box = QComboBox()
        for block in self.maintenance_blocks:
            line_combo_box.addItem(f"{block[0]} - Block #{block[1]}")
        h_layout.addWidget(line_combo_box)

        # Create 'Submit' button
        button = QPushButton("Submit")
        button.clicked.connect(lambda: self.submit_opening(dialog, line_combo_box.currentText()))
        h_layout.addWidget(button)

        # Add horizontal layout to the main layout
        layout.addLayout(h_layout)

        dialog.setLayout(layout)
        dialog.exec()

    # Handle the selection when 'Submit' is pressed
    def submit_opening(self, dialog, open_block):
        block_line, block_number_str = open_block.split(" - ")
        block_number_str = block_number_str[7:]
        block_number = int(block_number_str)
        block = (block_line, block_number)
        self.open_blocks.append(block)
        self.open_blocks = sorted(self.open_blocks, key=lambda x: x[1])
        self.maintenance_blocks.remove(block)
        self.update_opening_button_state()
        self.occupied_blocks.remove(block)

        print("Block", block_line, "on the", block_number, "line has been reopened from maintenance!")
        dialog.accept() 

    # Method to update the Opening button's state dynamically
    def update_opening_button_state(self):
        try:
            # Try disconnecting the clicked signal if it's already connected
            self.opening_button.clicked.disconnect()
        except TypeError:
            # If there's nothing to disconnect, just pass
            pass

        # Update the button's state based on whether there are maintenance blocks
        if len(self.maintenance_blocks) > 0:
            self.opening_button.setEnabled(True)
            self.opening_button.setStyleSheet("background-color: green; color: black;")
            self.opening_button.clicked.connect(self.openingClicked)  # Enable click functionality
        else:
            self.opening_button.setEnabled(False)  # Disable the button
            self.opening_button.setStyleSheet("background-color: gray; color: white;")