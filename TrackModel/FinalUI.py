import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget, QLineEdit, QComboBox, QLabel, QTableView, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
from TrackModel import buildTrack
from Section import Section
from Train import Train

redYard = [] 
redBlocks = []
redSwitches = []
redRailroadCrossing = []
redBeacons = [] 
redStations = [] 
redSections = []
greenYard = []
greenBlocks = [] 
greenSwitches = [] 
greenRailroadCrossings = []
greenBeacons = []
greenStations = []
greenSections = []

Trains = []
post_dict = []

class TrackUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100, 100, 850, 550)
        self.setStyleSheet("background-color: grey")
        
        # Initialize variables to store input
        self.input_value1 = ""
        self.input_value2 = ""

        # Create a font for labels and inputs
        big_font = QFont("Arial", 14)

        # Create labels
        self.label1 = QLabel("Red Track Excel Data", self)
        self.label1.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label1.setFont(big_font)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label1.setGeometry(165, 100, 210, 40)  # Position: (x=100, y=50), Size: (width=210, height=30)

        self.label2 = QLabel("Green Track Excel Data", self)
        self.label2.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label2.setFont(big_font)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label2.setGeometry(475, 100, 210, 40)  # Position: (x=400, y=50), Size: (width=210, height=30)

        # First text entry with custom position and size
        self.text_entry1 = QLineEdit(self)
        self.text_entry1.setFont(big_font)
        self.text_entry1.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry1.setPlaceholderText("Enter first value")
        self.text_entry1.setText("RedLine.xlsx")
        self.text_entry1.setGeometry(150, 150, 240, 40)  # Position: (x=100, y=100), Size: (width=230, height=40)

        # Second text entry with custom position and size
        self.text_entry2 = QLineEdit(self)
        self.text_entry2.setFont(big_font)
        self.text_entry2.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry2.setPlaceholderText("Enter second value")
        self.text_entry2.setText("GreenLine.xlsx")
        self.text_entry2.setGeometry(460, 150, 240, 40)  # Position: (x=400, y=100), Size: (width=230, height=40)

        # Save button with custom position and size
        self.button = QPushButton("Build Track", self)
        self.button.setStyleSheet("background-color: #772CE8; color: black")
        self.button.setFont(big_font)
        self.button.setGeometry(365, 240, 120, 50)  # Position: (x=325, y=200), Size: (width=120, height=50)
        self.button.clicked.connect(self.save_text)

    def save_text(self):
        global redYard, redBlocks, redSwitches, redRailroadCrossing, redBeacons, redStations, redSections
        global greenYard, greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations, greenSections
        global Train1
        # Store text entry values in separate variables
        self.input_value1 = self.text_entry1.text()
        self.input_value2 = self.text_entry2.text()

        #Red Line initial prep
        redYard, redBlocks, redSwitches, redRailroadCrossing, redBeacons, redStations = buildTrack(self.input_value1)

        redSections = []
        redSections.append(Section('A'))
        redSections.append(Section('B'))
        redSections.append(Section('C'))
        redSections.append(Section('D'))
        redSections.append(Section('E'))
        redSections.append(Section('F'))
        redSections.append(Section('G'))
        redSections.append(Section('H'))
        redSections.append(Section('I'))
        redSections.append(Section('J'))

        for i in range(76):
            if i >= 0 and i < 9:
                redSections[0].add_block(redBlocks[i])
            elif i >= 9 and i < 15:
                redSections[1].add_block(redBlocks[i])
            elif i >= 15 and i < 27:
                redSections[2].add_block(redBlocks[i])
            elif i >= 27 and i < 32:
                redSections[3].add_block(redBlocks[i])
            elif i >= 32 and i < 38:
                redSections[4].add_block(redBlocks[i])
            elif i >= 38 and i < 43:
                redSections[5].add_block(redBlocks[i])
            elif i >= 43 and i < 52:
                redSections[6].add_block(redBlocks[i])
            elif i >= 52 and i < 66:
                redSections[7].add_block(redBlocks[i])
            elif i >= 66 and i < 71:
                redSections[8].add_block(redBlocks[i])
            elif i >= 71 and i < 76:
                redSections[9].add_block(redBlocks[i])
            
        greenYard, greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations = buildTrack(self.input_value2)
        for i in range(150):
            greenBlocks[i].set_cmd_speed(70)
        greenBlocks[80].set_authority(1446.6)
        
        greenSections = []
        greenSections.append(Section('A'))
        greenSections.append(Section('B'))
        greenSections.append(Section('C'))
        greenSections.append(Section('D'))
        greenSections.append(Section('E'))
        greenSections.append(Section('F'))
        greenSections.append(Section('G'))
        greenSections.append(Section('H'))
        greenSections.append(Section('I'))
        greenSections.append(Section('J'))
        for i in range(150):
            if i >= 0 and i < 12:
                greenSections[0].add_block(greenBlocks[i])
            elif i >= 12 and i < 28:
                greenSections[1].add_block(greenBlocks[i])
            elif i >= 28 and i < 57:
                greenSections[2].add_block(greenBlocks[i])
            elif i >= 57 and i < 62:
                greenSections[3].add_block(greenBlocks[i])
            elif i >= 62 and i < 76:
                greenSections[4].add_block(greenBlocks[i])
            elif i >= 76 and i < 85:
                greenSections[5].add_block(greenBlocks[i])
            elif i >= 85 and i < 100:
                greenSections[6].add_block(greenBlocks[i])
            elif i >= 100 and i < 117:
                greenSections[7].add_block(greenBlocks[i])
            elif i >= 117 and i < 135:        
                greenSections[8].add_block(greenBlocks[i])
            elif i >= 135 and i < 150:
                greenSections[9].add_block(greenBlocks[i])   
        
            
        #Train
        temp_dict = {"authority" : None, "commanded_speed" : None, "beacon_info" : ""}
        Trains.append(Train(10, greenBlocks[80], 20))
        post_dict.append(temp_dict)

        self.ui_window = MainWindow()
        self.ui_window = self.ui_window.show()    
        self.close() 
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global redYard, redBlocks, redSwitches, redRailroadCrossing, redBeacons, redStations, redSections
        global greenYard, greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations, greenSections
        
        #Make a PyQt Window
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100,100,850,550)
        self.setStyleSheet("background-color: grey")

        #Makes tabs for the windows
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.create_tabs()

        #All updating functions, updated every .1 second
        self.train_timer = QTimer()
        #Does the train movement 
        self.train_timer.timeout.connect(Train1.moveTrain)

        self.train_timer.start(1)#10

    def get_post_dict(self):
        return {"data": post_dict}

    def create_tabs(self):
        #Tab 3 for green line
        tab4 = QWidget()
        self.tab_widget.addTab(tab4, "Green Line")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_green_sections(tab4, -100, 50)

        self.make_green_switches(tab4, -100, 50)

        # self.make_lights(tab1, 110)

        self.make_green_crossings(tab4, 0, 0)

        self.make_train(tab4)

        self.make_green_stations(tab4, 0, 0)

        # self.make_beacons(tab1)

        # self.make_failure_buttons(tab1)
    
        #Tab 5 for table info 
        tab5 = QWidget()
        self.tab_widget.addTab(tab5, "Green Track Info")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_green_table(tab5)

        #Tab 4 for test bench
        #input track changes here
        tab6 = QWidget()
        self.tab_widget.addTab(tab6, "Green Test Bench")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_green_test_bench(tab6, -30)

        #Create Tab 1 red line
        tab1 = QWidget()
        self.tab_widget.addTab(tab1, "Red Line")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_red_sections(tab1, 0, 0)

        self.make_red_switches(tab1, 0, 0)

        # self.make_lights(tab1, 110)

        # self.make_crossing(tab1, 110)

        # self.make_train(tab1)

        # self.make_stations(tab1)

        # self.make_beacons(tab1)

        # self.make_failure_buttons(tab1)

        #Tab 2 for table info 
        tab2 = QWidget()
        self.tab_widget.addTab(tab2, "Red Track Info")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_red_table(tab2)

        #Tab 3 for test bench
        #input track changes here
        tab3 = QWidget()
        self.tab_widget.addTab(tab3, "Red Test Bench")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_red_test_bench(tab3, -30)

    def make_red_table(self, tab):
        self.red_block_table = QStandardItemModel(len(redBlocks), 15)
        self.red_block_table.setHorizontalHeaderLabels(["Section", "Occupied", "Authority", "Commanded Speed", "Beacon", "Station", "Railroad", "Switch", "Traffic Light", "Next Block", "Previous Block", "Length", "Grade", "Speed Limit", "Elevation", "Cum. Elevation", "Underground", "Broken Track", "Circuit Failure", "Power Failure"])
        self.populate_red_table()

        red_block_table_view = QTableView()
        red_block_table_view.setModel(self.red_block_table)

        layout = QVBoxLayout()
        layout.addWidget(red_block_table_view)
        tab.setLayout(layout)

    def populate_red_table(self):
        for row in range(len(redBlocks)):
            for col in range(20):
                value = redBlocks[row].get_table_data(col)
                item = QStandardItem(value)
                self.red_block_table.setItem(row, col, item)
                if col == 1:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 14:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 15:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 16:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 17:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                else:
                    item.setBackground(Qt.GlobalColor.darkGray)

    def make_green_table(self, tab):
        self.green_block_table = QStandardItemModel(len(greenBlocks), 20)
        self.green_block_table.setHorizontalHeaderLabels(["Section", "Occupied", "Authority", "Commanded Speed", "Beacon", "Station", "Railroad", "Switch", "Traffic Light", "Next Block", "Previous Block", "Length", "Grade", "Speed Limit", "Elevation", "Cum. Elevation", "Underground", "Broken Track", "Circuit Failure", "Power Failure"])
        self.populate_green_table()

        green_block_table_view = QTableView()
        green_block_table_view.setModel(self.green_block_table)
        
        layout = QVBoxLayout()
        layout.addWidget(green_block_table_view)
        tab.setLayout(layout)
    
    def populate_green_table(self):
        for row in range(len(greenBlocks)):
            for col in range(20):
                value = greenBlocks[row].get_table_data(col)
                item = QStandardItem(value)
                self.green_block_table.setItem(row, col, item)
                if col == 1:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 14:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 15:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 16:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                elif col == 17:
                    if value == "True":
                        item.setBackground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setBackground(Qt.GlobalColor.darkGray)
                else:
                    item.setBackground(Qt.GlobalColor.darkGray)
                






    def update_red_ui(self):
        self.populate_red_table()
        #All "setToolTip" functions are updating the hover information for all objects
        #Constantly update block color based on occupied variable
        for i in range(10):
            #if occupied hide blue arrow, white is underneath
            redSections[i].check_occupied()
            if redSections[i].get_occupied():
                self.redArrows[i].hide()
            else:
                self.redArrows[i].show()
            index = i+1
            self.redArrows[i].setToolTip(redSections[i].display_info())
            self.underRedArrows[i].setToolTip(redSections[i].display_info())
        # #Constantly update switch direction based on left or right variable
        for i in range(7):
            if redSwitches[i].get_LorR():
                self.leftRedSwitches[i].hide()
                self.rightRedSwitches[i].show()
            else:
                self.leftRedSwitches[i].show()
                self.rightRedSwitches[i].hide()
            self.leftRedSwitches[i].setToolTip(redSwitches[i].display_info(0))
            self.rightRedSwitches[i].setToolTip(redSwitches[i].display_info(0))

        # #Constantly update traffic light color based on red or green variable
        # for i in range(2):
        #     #red is underneath green
        #     if blueTrafficLights[i].get_RorG():
        #         self.greenLight[i].show()
        #     else:
        #         self.greenLight[i].hide()
        #     self.greenLight[i].setToolTip(blueTrafficLights[i].display_info(i))
        #     self.redLight[i].setToolTip(blueTrafficLights[i].display_info(i))
            
        # #Constantly update railroad crossing color based on up or down variable
        # if blueRailroadCrossing.get_UorD():
        #     self.greenCrossing.hide()
        # else:
        #     self.greenCrossing.show()
        # self.greenCrossing.setToolTip(blueRailroadCrossing.display_info(0))
        # self.redCrossing.setToolTip(blueRailroadCrossing.display_info(0))

        # self.trainLabel.setToolTip(blueTrain.display_info(0))

        # self.stations[0].setToolTip(blueStations[0].display_info())
        # self.stations[1].setToolTip(blueStations[1].display_info())

        # self.beacons[0].setToolTip(blueBeacons[0].display_info())
        # self.beacons[1].setToolTip(blueBeacons[1].display_info())

    def update_green_ui(self):
        self.populate_green_table()
        
        for i in range(150):
            greenBlocks[i].set_occupancies()
        #All "setToolTip" functions are updating the hover information for all objects
        #Constantly update block color based on occupied variable
        for i in range(10):
            #if occupied hide blue arrow, white is underneath
            greenSections[i].check_occupied()
            if greenSections[i].get_occupied():
                self.greenArrows[i].hide()
            else:
                self.greenArrows[i].show()
            self.greenArrows[i].setToolTip(greenSections[i].display_info())
            self.underGreenArrows[i].setToolTip(greenSections[i].display_info())
        # #Constantly update switch direction based on left or right variable
        for i in range(6):
            if greenSwitches[i].get_LorR():
                self.leftGreenSwitches[i].hide()
                self.rightGreenSwitches[i].show()
            else:
                self.leftGreenSwitches[i].show()
                self.rightGreenSwitches[i].hide()
            self.leftGreenSwitches[i].setToolTip(greenSwitches[i].display_info(0))
            self.rightGreenSwitches[i].setToolTip(greenSwitches[i].display_info(0))

        # #Constantly update traffic light color based on red or green variable
        # for i in range(2):
        #     #red is underneath green
        #     if blueTrafficLights[i].get_RorG():
        #         self.greenLight[i].show()
        #     else:
        #         self.greenLight[i].hide()
        #     self.greenLight[i].setToolTip(blueTrafficLights[i].display_info(i))
        #     self.redLight[i].setToolTip(blueTrafficLights[i].display_info(i))
            
        #Constantly update railroad crossing color based on up or down variable
        for i in range(2):
            if greenRailroadCrossings[i].get_UorD():
                self.greenCrossings[i].hide()
            else:
                self.greenCrossings[i].show()
            self.greenCrossings[i].setToolTip(greenRailroadCrossings[i].display_info(0))
            self.redCrossings[i].setToolTip(greenRailroadCrossings[i].display_info(0))

        self.trainLabel.setToolTip(Train1.display_info(0))

        for i in range(18):
            if greenStations[i].get_trainIn():
                self.stations[i].hide()
            else:
                self.stations[i].show()
            self.stationsBot[i].setToolTip(greenStations[i].display_info())
            self.stations[i].setToolTip(greenStations[i].display_info())

        # self.beacons[0].setToolTip(blueBeacons[0].display_info())
        # self.beacons[1].setToolTip(blueBeacons[1].display_info())

    def make_red_test_bench(self, tab2, x):
        #Column 1 input text
        idStrings = ['Switch ID', 'Crossing Light ID', 'Traffic Light ID', 'Block ID', 'Block ID', 'Block ID']
        self.idLabels = []
        self.idInputs = []
        #Column 2 input text
        varStrings = ['Left or Right', 'Up or Down', 'Red or Green', 'Authority (m)', 'Cmnd Speed (kmph)', 'Occupation']
        self.varLabels = []
        self.varInputs = []
        self.sendButtons = [] 
        #For all 6 test bench inputs
        for i in range(6):
            #Col 1 labels
            self.idLabels.append(QLabel(idStrings[i], tab2))
            self.idLabels[i].setStyleSheet("color: white;")
            self.idLabels[i].setGeometry(10-x, 40 + 40 * i, 100, 20)

            #Col 1 inputs
            self.idInputs.append(QLineEdit(tab2))
            self.idInputs[i].setStyleSheet("background-color: white; color: black;")
            self.idInputs[i].setGeometry(10-x, 60 + 40 * i, 90, 20)

            #Col 2 labels
            self.varLabels.append(QLabel(varStrings[i], tab2))
            self.varLabels[i].setStyleSheet("color: white;")
            self.varLabels[i].setGeometry(110-x, 40 + 40 * i, 140, 20)

            #Send buttons for each test bench input
            self.sendButtons.append(QPushButton("Send", tab2))
            self.sendButtons[i].setStyleSheet("background-color: white; color: black;")
            self.sendButtons[i].clicked.connect(lambda _, index=i: self.send_red_button_click(index))
            self.sendButtons[i].setGeometry(220-x, 60 + 40 * i, 50, 20)           
        
        #Col 2 inputs must be indiividually done because they have different formats for bools
        self.varInputs.append(QComboBox(tab2))
        self.varInputs[0].addItems(['Left', 'Right'])
        self.varInputs[0].setStyleSheet("background-color: white; color: black;")
        self.varInputs[0].setGeometry(110-x, 60 + 40 * 0, 100, 20)

        self.varInputs.append(QComboBox(tab2))
        self.varInputs[1].addItems(['Up', 'Down'])
        self.varInputs[1].setStyleSheet("background-color: white; color: black;")
        self.varInputs[1].setGeometry(110-x, 60 + 40 * 1, 100, 20)

        self.varInputs.append(QComboBox(tab2))
        self.varInputs[2].addItems(['Red', 'Green'])
        self.varInputs[2].setStyleSheet("background-color: white; color: black;")
        self.varInputs[2].setGeometry(110-x, 60 + 40 * 2, 100, 20)

        self.varInputs.append(QLineEdit(tab2))
        self.varInputs[3].setStyleSheet("background-color: white; color: black;")
        self.varInputs[3].setGeometry(110-x, 60 + 40 * 3, 100, 20)

        self.varInputs.append(QLineEdit(tab2))
        self.varInputs[4].setStyleSheet("background-color: white; color: black;")
        self.varInputs[4].setGeometry(110-x, 60 + 40 * 4, 100, 20)

        self.varInputs.append(QComboBox(tab2))
        self.varInputs[5].addItems(['Not Occupied', 'Occupied'])
        self.varInputs[5].setStyleSheet("background-color: white; color: black;")
        self.varInputs[5].setGeometry(110-x, 60 + 40 * 5, 100, 20)

    def send_red_button_click(self, i):
        #test bench button clicked, a specific input must be processed
        #Column 1 (which is always some form of int ID)
        id = int(self.idInputs[i].text())
        #Column 2 which can be... 
        if (i == 3 or i == 4):
            #... String text ...
            var = self.varInputs[i].text()
        else:
            #... or bool option selections
            var = self.varInputs[i].currentText()
        #if row 1 input for switch changes
        if i == 0:
            if id >= 0 and id < 7:
                if var == "Left":
                    redSwitches[id].set_L()
                else:
                    redSwitches[id].set_R()
            else:
                print("Index Error sendButton_click function.")
        #if row 2 input for railroad crossings
        elif i == 1:
            if id == 0:
                if var == "Up":
                    redRailroadCrossing[id].set_U()
                else:
                    redRailroadCrossing[id].set_D()
            else:
                print("Index Error sendButton_click function.")
        #if row 3 input for traffic lights
        elif i == 2:
            print("No traffic lights")
        #     if id <= 1 and id >= 0:
        #         if var == "Red":
        #             redTrafficLights[id].set_R()
        #         else:
        #             blueTrafficLights[id].set_G()
        #     else:
        #         print("Index Error sendButton_click function.")
        # #if row 4 input authority for specific block changes
        elif i == 3:
            if id <= 76 and id >= 1:
                print(f"Authority on block {id} set to {var} m")
            else:
                print("error")
        #if row 5 input commanded speed for specific block changes
        elif i == 4:
            if id <= 76 and id >= 1:
                print(f"Commanded Speed on block {id} set to {var} km/h")
            else:
                print("Index Error sendButton_click function.")
        #if row 6 input change a blocks occupancy
        elif i == 5:
            if id <= 76 and id >= 1:
                if var == "Occupied":
                    redBlocks[id-1].set_O()
                else:
                    redBlocks[id-1].set_N()
            else:
                print("Index Error sendButton_click function.")

    def make_green_test_bench(self, tab4, x):
        #Column 1 input text
        idStrings = ['Switch ID', 'Crossing Light ID', 'Traffic Light ID', 'Block ID', 'Block ID', 'Block ID']
        self.idLabels = []
        self.idInputs = []
        #Column 2 input text
        varStrings = ['Left or Right', 'Up or Down', 'Red or Green', 'Authority (m)', 'Cmnd Speed (kmph)', 'Occupation']
        self.varLabels = []
        self.varInputs = []
        self.sendButtons = [] 
        #For all 6 test bench inputs
        for i in range(6):
            #Col 1 labels
            self.idLabels.append(QLabel(idStrings[i], tab4))
            self.idLabels[i].setStyleSheet("color: white;")
            self.idLabels[i].setGeometry(10-x, 40 + 40 * i, 100, 20)

            #Col 1 inputs
            self.idInputs.append(QLineEdit(tab4))
            self.idInputs[i].setStyleSheet("background-color: white; color: black;")
            self.idInputs[i].setGeometry(10-x, 60 + 40 * i, 90, 20)

            #Col 2 labels
            self.varLabels.append(QLabel(varStrings[i], tab4))
            self.varLabels[i].setStyleSheet("color: white;")
            self.varLabels[i].setGeometry(110-x, 40 + 40 * i, 140, 20)

            #Send buttons for each test bench input
            self.sendButtons.append(QPushButton("Send", tab4))
            self.sendButtons[i].setStyleSheet("background-color: white; color: black;")
            self.sendButtons[i].clicked.connect(lambda _, index=i: self.send_green_button_click(index))
            self.sendButtons[i].setGeometry(220-x, 60 + 40 * i, 50, 20)           
        
        #Col 2 inputs must be indiividually done because they have different formats for bools
        self.varInputs.append(QComboBox(tab4))
        self.varInputs[0].addItems(['Left', 'Right'])
        self.varInputs[0].setStyleSheet("background-color: white; color: black;")
        self.varInputs[0].setGeometry(110-x, 60 + 40 * 0, 100, 20)

        self.varInputs.append(QComboBox(tab4))
        self.varInputs[1].addItems(['Up', 'Down'])
        self.varInputs[1].setStyleSheet("background-color: white; color: black;")
        self.varInputs[1].setGeometry(110-x, 60 + 40 * 1, 100, 20)

        self.varInputs.append(QComboBox(tab4))
        self.varInputs[2].addItems(['Red', 'Green'])
        self.varInputs[2].setStyleSheet("background-color: white; color: black;")
        self.varInputs[2].setGeometry(110-x, 60 + 40 * 2, 100, 20)

        self.varInputs.append(QLineEdit(tab4))
        self.varInputs[3].setStyleSheet("background-color: white; color: black;")
        self.varInputs[3].setGeometry(110-x, 60 + 40 * 3, 100, 20)

        self.varInputs.append(QLineEdit(tab4))
        self.varInputs[4].setStyleSheet("background-color: white; color: black;")
        self.varInputs[4].setGeometry(110-x, 60 + 40 * 4, 100, 20)

        self.varInputs.append(QComboBox(tab4))
        self.varInputs[5].addItems(['Not Occupied', 'Occupied'])
        self.varInputs[5].setStyleSheet("background-color: white; color: black;")
        self.varInputs[5].setGeometry(110-x, 60 + 40 * 5, 100, 20)

    def send_green_button_click(self, i):
        #test bench button clicked, a specific input must be processed
        #Column 1 (which is always some form of int ID)
        id = int(self.idInputs[i].text())
        #Column 2 which can be... 
        if (i == 3 or i == 4):
            #... String text ...
            var = self.varInputs[i].text()
        else:
            #... or bool option selections
            var = self.varInputs[i].currentText()
        #if row 1 input for switch changes
        if i == 0:
            if id >= 0 and id < 6:
                if var == "Left":
                    greenSwitches[id].set_L()
                else:
                    greenSwitches[id].set_R()
            else:
                print("Index Error sendButton_click function.")
        #if row 2 input for railroad crossings
        elif i == 1:
            if id == 0:
                if var == "Up":
                    greenRailroadCrossings[id].set_U()
                else:
                    greenRailroadCrossings[id].set_D()
            else:
                print("Index Error sendButton_click function.")
        #if row 3 input for traffic lights
        elif i == 2:
            print("No traffic lights")
        #     if id <= 1 and id >= 0:
        #         if var == "Red":
        #             redTrafficLights[id].set_R()
        #         else:
        #             blueTrafficLights[id].set_G()
        #     else:
        #         print("Index Error sendButton_click function.")
        # #if row 4 input authority for specific block changes
        elif i == 3:
            if id <= 150 and id >= 1:
                greenBlocks[id-1].set_authority(float(var))
            else:
                print("Index Error")
        #if row 5 input commanded speed for specific block changes
        elif i == 4:
            if id <= 150 and id >= 1:
                greenBlocks[id-1].set_cmd_speed(float(var))
            else:
                print("Index Error sendButton_click function.")
        #if row 6 input change a blocks occupancy
        elif i == 5:
            if id <= 150 and id >= 1:
                if var == "Occupied":
                    greenBlocks[id-1].set_O()
                else:
                    greenBlocks[id-1].set_N()
            else:
                print("Index Error sendButton_click function.")

    # def make_failure_buttons(self, tab1):
    #     self.failureButtons = []
    #     failureText = ['Broken Track', 'Track Circuit Failure', 'Power Failure']
    #     for i in range(3):
    #         self.failureButtons.append(QPushButton(failureText[i], tab1))
    #         self.failureButtons[i].setStyleSheet("background-color: white; color: black;")
    #         self.failureButtons[i].clicked.connect(lambda _, index=i: self.send_failure_button_click(index))
    #         self.failureButtons[i].setGeometry(220, 230 + 30 * i, 120, 25)  

    #     self.blockNum = QLineEdit(tab1)
    #     self.blockNum.setStyleSheet("background-color: white; color: black;")
    #     self.blockNum.setGeometry(220, 200, 70, 25)

    #     self.blockLabel = QLabel('Block Number:', tab1)
    #     self.blockLabel.setStyleSheet("color: white;")
    #     self.blockLabel.setGeometry(220, 180, 100, 20)

    # def send_failure_button_click(self, i): 
    #     num = int(self.blockNum.text()) - 1 
    #     if num >= 0 and num <= 15:    
    #         if i == 0:
    #             blueBlocks[num].change_broken()
    #         elif i == 1:
    #             blueBlocks[num].change_circuit()
    #         elif i == 2:
    #             blueBlocks[num].change_power()

    def make_red_sections(self, tab1, x, y):
        #White arrows are behind blue arrows so you can show or hide the blue arrows
        self.underRedArrows = []
        self.redArrows = []
        original_pixmap_white = QPixmap("images/WhiteFlatArrow.png")
        resized_pixmap_white = original_pixmap_white.scaled(60,30)
        original_pixmap_blue = QPixmap("images/RedFlatArrow.png")
        resized_pixmap_blue = original_pixmap_blue.scaled(60,30)
        for i in range(10):
            self.underRedArrows.append(QLabel(tab1))
            self.underRedArrows[i].setPixmap(resized_pixmap_white)
            
            self.redArrows.append(QLabel(tab1))
            self.redArrows[i].setPixmap(resized_pixmap_blue)
            
        self.underRedArrows[0].setGeometry(183+x, 17+y, 60, 30)
        self.redArrows[0].setGeometry(183+x, 17+y, 60, 30)
        self.underRedArrows[1].setGeometry(183+x, 120+y, 60, 30)
        self.redArrows[1].setGeometry(183+x, 120+y, 60, 30)

        self.underRedArrows[2].setGeometry(333+x, 67+y, 60, 30)
        self.redArrows[2].setGeometry(333+x, 67+y, 60, 30)

        self.underRedArrows[3].setGeometry(473+x, 17+y, 60, 30)
        self.redArrows[3].setGeometry(473+x, 17+y, 60, 30)
        self.underRedArrows[9].setGeometry(473+x, 120+y, 60, 30)
        self.redArrows[9].setGeometry(473+x, 120+y, 60, 30)

        self.underRedArrows[4].setGeometry(600+x, 140+y, 60, 30)
        self.redArrows[4].setGeometry(600+x, 140+y, 60, 30)


        self.underRedArrows[8].setGeometry(473+x, 177+y, 60, 30)
        self.redArrows[8].setGeometry(473+x, 177, 60+y, 30)
        self.underRedArrows[5].setGeometry(473+x, 280+y, 60, 30)
        self.redArrows[5].setGeometry(473+x, 280+y, 60, 30)

        self.underRedArrows[6].setGeometry(333+x, 227+y, 60, 30)
        self.redArrows[6].setGeometry(333+x, 227+y, 60, 30)

        self.underRedArrows[7].setGeometry(183+x, 227+y, 60, 30)
        self.redArrows[7].setGeometry(183+x, 227+y, 60, 30)

        #this is the timer that constantly updates the states for all of the components 
        self.red_timer = QTimer()
        self.red_timer.timeout.connect(self.update_red_ui)
        self.red_timer.start(100)

    def make_green_sections(self, tab3, x, y):
        #White arrows are behind blue arrows so you can show or hide the blue arrows
        self.underGreenArrows = []
        self.greenArrows = []
        original_pixmap_white = QPixmap("images/WhiteFlatArrow.png")
        resized_pixmap_white = original_pixmap_white.scaled(60,30)
        original_pixmap_green = QPixmap("images/GreenFlatArrow.png")
        resized_pixmap_green = original_pixmap_green.scaled(60,30)
        original_tester = QPixmap("images/SizeTester.png")
        section0_top = QPixmap("images/GreenSection0Top.png")
        section0_top = section0_top.scaled(107,123)
        section0_bot = QPixmap("images/GreenSection0Bot.png")
        section0_bot = section0_bot.scaled(107,123)
        section1_top = QPixmap("images/GreenSection1Top.png")
        section1_top = section1_top.scaled(129,30)
        section1_bot = QPixmap("images/GreenSection1Bot.png")
        section1_bot = section1_bot.scaled(129,30)
        section2_top = QPixmap("images/GreenSection2Top.png")
        section2_top = section2_top.scaled(213,30)
        section2_bot = QPixmap("images/GreenSection2Bot.png")
        section2_bot = section2_bot.scaled(213,30)
        section3_top = QPixmap("images/GreenSection3Top.png")
        section3_top = section3_top.scaled(30,183)
        section3_bot = QPixmap("images/GreenSection3Bot.png")
        section3_bot = section3_bot.scaled(30,183)
        section4_top = QPixmap("images/GreenSection4Top.png")
        section4_top = section4_top.scaled(207,30)
        section4_bot = QPixmap("images/GreenSection4Bot.png")
        section4_bot = section4_bot.scaled(207,30)
        section5_top = QPixmap("images/GreenSection5Top.png")
        section5_top = section5_top.scaled(57,30)
        section5_bot = QPixmap("images/GreenSection5Bot.png")
        section5_bot = section5_bot.scaled(57,30)
        section6_top = QPixmap("images/GreenSection0Top.png")
        section6_top = section6_top.scaled(107,123)
        section6_bot = QPixmap("images/GreenSection0Bot.png")
        section6_bot = section6_bot.scaled(107,123)
        section7_top = QPixmap("images/GreenSection7Top.png")
        section7_top = section7_top.scaled(149, 30)
        section7_bot = QPixmap("images/GreenSection7Bot.png")
        section7_bot = section7_bot.scaled(149, 30)
        section8_top = QPixmap("images/GreenSection8Top.png")
        section8_top = section8_top.scaled(30,156)
        section8_bot = QPixmap("images/GreenSection8Bot.png")
        section8_bot = section8_bot.scaled(30,156)
        section9_top = QPixmap("images/GreenSection9Top.png")
        section9_top = section9_top.scaled(103,30)
        section9_bot = QPixmap("images/GreenSection9Bot.png")
        section9_bot = section9_bot.scaled(103,30)
        for i in range(10):
            self.underGreenArrows.append(QLabel(tab3))
            self.underGreenArrows[i].setPixmap(resized_pixmap_white)
            
            self.greenArrows.append(QLabel(tab3))
            self.greenArrows[i].setPixmap(resized_pixmap_green)

        self.greenArrows[0].setPixmap(section0_top)  
        self.underGreenArrows[0].setPixmap(section0_bot)  
        self.underGreenArrows[0].setGeometry(762+x, 22+y, 107, 123)
        self.greenArrows[0].setGeometry(762+x, 22+y, 107, 123)

        self.greenArrows[1].setPixmap(section1_top)
        self.underGreenArrows[1].setPixmap(section1_bot)  
        self.underGreenArrows[1].setGeometry(548+x, 67+y, 129, 30)
        self.greenArrows[1].setGeometry(548+x, 67+y, 129, 30)

        self.greenArrows[2].setPixmap(section2_top)
        self.underGreenArrows[2].setPixmap(section2_bot)  
        self.underGreenArrows[2].setGeometry(273+x, 20+y, 190, 30)
        self.greenArrows[2].setGeometry(273+x, 20+y, 190, 30)

        self.greenArrows[3].setPixmap(section3_top)
        self.underGreenArrows[3].setPixmap(section3_bot)  
        self.underGreenArrows[3].setGeometry(244+x, 147+y, 30, 183)
        self.greenArrows[3].setGeometry(244+x, 147+y, 30, 183)

        self.greenArrows[4].setPixmap(section4_top)
        self.underGreenArrows[4].setPixmap(section4_bot)  
        self.underGreenArrows[4].setGeometry(332+x, 380+y, 207, 30)
        self.greenArrows[4].setGeometry(332+x, 380+y, 207, 30)

        self.greenArrows[5].setPixmap(section5_top)
        self.underGreenArrows[5].setPixmap(section5_bot)  
        self.underGreenArrows[5].setGeometry(622+x, 327+y, 58, 30)
        self.greenArrows[5].setGeometry(622+x, 327+y, 58, 30)

        self.greenArrows[6].setPixmap(section0_top)
        self.underGreenArrows[6].setPixmap(section6_bot)  
        self.underGreenArrows[6].setGeometry(762+x, 280+y, 107, 123)
        self.greenArrows[6].setGeometry(762+x, 280+y, 107, 123)

        self.greenArrows[7].setPixmap(section7_top)
        self.underGreenArrows[7].setPixmap(section7_bot)  
        self.underGreenArrows[7].setGeometry(391+x, 277+y, 149, 30)
        self.greenArrows[7].setGeometry(391+x, 277+y, 149, 30)

        self.greenArrows[8].setPixmap(section8_top)
        self.underGreenArrows[8].setPixmap(section8_bot)  
        self.underGreenArrows[8].setGeometry(360+x, 151+y, 30, 156)
        self.greenArrows[8].setGeometry(360+x, 151+y, 30, 156)

        self.greenArrows[9].setPixmap(section9_top)
        self.underGreenArrows[9].setPixmap(section9_bot)  
        self.underGreenArrows[9].setGeometry(360+x, 120+y, 103, 30)
        self.greenArrows[9].setGeometry(360+x, 120+y, 103, 30)

        #this is the timer that constantly updates the states for all of the components 
        self.green_timer = QTimer()
        self.green_timer.timeout.connect(self.update_green_ui)
        self.green_timer.start(100)

    def make_red_switches(self, tab3, x, y):
        self.leftRedSwitches = []
        self.rightRedSwitches = []
        original_pixmap_left = QPixmap("images/SwitchLeft.png")
        resized_pixmap_left = original_pixmap_left.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right = QPixmap("images/SwitchRight.png")
        resized_pixmap_right = original_pixmap_right.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_reversed = QPixmap("images/SwitchLeftReversed.png")
        resized_pixmap_left_reversed = original_pixmap_left_reversed.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_reversed = QPixmap("images/SwitchRightReversed.png")
        resized_pixmap_right_reversed = original_pixmap_right_reversed.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_red1 = QPixmap("images/SwitchLeftRed1.png")
        resized_pixmap_left_red1 = original_pixmap_left_red1.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_red1 = QPixmap("images/SwitchRightRed1.png")
        resized_pixmap_right_red1 = original_pixmap_right_red1.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[0].setPixmap(resized_pixmap_right_red1)
        self.leftRedSwitches[0].setGeometry(100+x, 20+y, 83, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[0].setPixmap(resized_pixmap_left_red1)
        self.rightRedSwitches[0].setGeometry(100+x, 20+y, 83, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[1].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[1].setGeometry(250+x, 20+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[1].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[1].setGeometry(250+x, 20+y, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[2].setPixmap(resized_pixmap_left)
        self.leftRedSwitches[2].setGeometry(390+x, 20+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[2].setPixmap(resized_pixmap_right)
        self.rightRedSwitches[2].setGeometry(390+x, 20+y, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[3].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[3].setGeometry(530+x, 20+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[3].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[3].setGeometry(530+x, 20+y, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[4].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[4].setGeometry(530+x, 180+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[4].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[4].setGeometry(530+x, 180+y, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[5].setPixmap(resized_pixmap_left)
        self.leftRedSwitches[5].setGeometry(390+x, 180+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[5].setPixmap(resized_pixmap_right)
        self.rightRedSwitches[5].setGeometry(390+x, 180+y, 80, 125)
        
        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[6].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[6].setGeometry(250+x, 180+y, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[6].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[6].setGeometry(250+x, 180+y, 80, 125)

    def make_green_switches(self, tab3, x, y):
        self.leftGreenSwitches = []
        self.rightGreenSwitches = []
        original_pixmap_left = QPixmap("images/SwitchLeft.png")
        resized_pixmap_left = original_pixmap_left.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right = QPixmap("images/SwitchRight.png")
        resized_pixmap_right = original_pixmap_right.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_reversed = QPixmap("images/SwitchLeftReversed.png")
        resized_pixmap_left_reversed = original_pixmap_left_reversed.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_reversed = QPixmap("images/SwitchRightReversed.png")
        resized_pixmap_right_reversed = original_pixmap_right_reversed.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_red1 = QPixmap("images/SwitchLeftRed1.png")
        resized_pixmap_left_red1 = original_pixmap_left_red1.scaled(83,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_red1 = QPixmap("images/SwitchRightRed1.png")
        resized_pixmap_right_red1 = original_pixmap_right_red1.scaled(83,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[0].setPixmap(resized_pixmap_left)
        self.leftGreenSwitches[0].setGeometry(680+x, 20+y, 80, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[0].setPixmap(resized_pixmap_right)
        self.rightGreenSwitches[0].setGeometry(680+x, 20+y, 80, 125)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[1].setPixmap(resized_pixmap_left_reversed)
        self.leftGreenSwitches[1].setGeometry(465+x, 20+y, 80, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[1].setPixmap(resized_pixmap_right_reversed)
        self.rightGreenSwitches[1].setGeometry(465+x, 20+y, 80, 125)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[2].setPixmap(resized_pixmap_right_red1)
        self.leftGreenSwitches[2].setGeometry(190+x, 20+y, 83, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[2].setPixmap(resized_pixmap_left_red1)
        self.rightGreenSwitches[2].setGeometry(190+x, 20+y, 83, 125)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[3].setPixmap(resized_pixmap_left_reversed)
        self.leftGreenSwitches[3].setGeometry(250+x, 330+y, 80, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[3].setPixmap(resized_pixmap_right_reversed)
        self.rightGreenSwitches[3].setGeometry(250+x, 330+y, 80, 125)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[4].setPixmap(resized_pixmap_left_reversed)
        self.leftGreenSwitches[4].setGeometry(540+x, 280+y, 80, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[4].setPixmap(resized_pixmap_right_reversed)
        self.rightGreenSwitches[4].setGeometry(540+x, 280+y, 80, 125)

        self.leftGreenSwitches.append(QLabel(tab3))
        self.leftGreenSwitches[5].setPixmap(resized_pixmap_left)
        self.leftGreenSwitches[5].setGeometry(680+x, 280+y, 80, 125)
        self.rightGreenSwitches.append(QLabel(tab3))
        self.rightGreenSwitches[5].setPixmap(resized_pixmap_right)
        self.rightGreenSwitches[5].setGeometry(680+x, 280+y, 80, 125)

    # def make_lights(self, tab1, x):
    #     original_pixmap_red = QPixmap("images/RedLight.png")
    #     resized_pixmap_red = original_pixmap_red.scaled(40,40)
    #     original_pixmap_green = QPixmap("images/GreenLight.png")
    #     resized_pixmap_green = original_pixmap_green.scaled(40,40)
    #     self.redLight = []
    #     self.greenLight = []
    #     self.redLight.append(QLabel(tab1))
    #     self.redLight.append(QLabel(tab1))
    #     self.redLight[0].setPixmap(resized_pixmap_red)
    #     self.redLight[1].setPixmap(resized_pixmap_red)
    #     self.redLight[0].setGeometry(435, 150-x, 40, 40)
    #     self.redLight[1].setGeometry(435, 340-x, 40, 40)
    #     self.greenLight.append(QLabel(tab1))
    #     self.greenLight.append(QLabel(tab1))
    #     self.greenLight[0].setPixmap(resized_pixmap_green)
    #     self.greenLight[1].setPixmap(resized_pixmap_green)
    #     self.greenLight[0].setGeometry(435, 150-x, 40, 40)
    #     self.greenLight[1].setGeometry(435, 340-x, 40, 40)

    def make_green_crossings(self, tab3, x, y):
        original_pixmap_red = QPixmap("images/RedCrossing.png")
        resized_pixmap_red = original_pixmap_red.scaled(50,50)
        original_pixmap_green = QPixmap("images/GreenCrossing.png")
        resized_pixmap_green = original_pixmap_green.scaled(50,50)
        self.redCrossings = []
        self.greenCrossings = []

        self.redCrossings.append(QLabel(tab3))
        self.redCrossings[0].setPixmap(resized_pixmap_red)
        self.redCrossings[0].setGeometry(450, 145, 50, 50)
        self.greenCrossings.append(QLabel(tab3))
        self.greenCrossings[0].setPixmap(resized_pixmap_green)
        self.greenCrossings[0].setGeometry(450, 145, 50, 50)

        self.redCrossings.append(QLabel(tab3))
        self.redCrossings[0].setPixmap(resized_pixmap_red)
        self.redCrossings[0].setGeometry(450, 150, 50, 50)
        self.greenCrossings.append(QLabel(tab3))
        self.greenCrossings[0].setPixmap(resized_pixmap_green)
        self.greenCrossings[0].setGeometry(450, 150, 50, 50)
    
    def make_train(self, tab3):
        self.trainLabel = QPushButton("Train Info", tab3)
        self.trainLabel.setStyleSheet("background-color: white; color: black;")
        self.trainLabel.setGeometry(50,40, 80, 25)

    def make_green_stations(self,tab1,x, y):
        original_pixmap_station = QPixmap("images/Station.png")
        resized_pixmap_station = original_pixmap_station.scaled(53,38)
        original_pixmap_station_bot = QPixmap("images/StationBot.png")
        resized_pixmap_station_bot = original_pixmap_station_bot.scaled(53,38)
        self.stations = []
        self.stationsBot = []
        for i in range(18):
            self.stationsBot.append(QLabel(tab1))
            self.stationsBot[i].setPixmap(resized_pixmap_station_bot)
            self.stations.append(QLabel(tab1))
            self.stations[i].setPixmap(resized_pixmap_station)
        self.stationsBot[0].setGeometry(680+x, 32+y, 53, 38)
        self.stationsBot[1].setGeometry(770+x, 100+y, 53, 38)
        self.stationsBot[2].setGeometry(520+x, 75+y, 53, 38)
        self.stationsBot[3].setGeometry(450+x, 75+y, 53, 38)
        self.stationsBot[4].setGeometry(305+x, 32+y, 53, 38)
        self.stationsBot[5].setGeometry(237+x, 32+y, 53, 38)
        self.stationsBot[6].setGeometry(204+x, 100+y, 53, 38)
        self.stationsBot[7].setGeometry(170+x, 32+y, 53, 38)
        self.stationsBot[8].setGeometry(240+x, 460+y, 53, 38)
        self.stationsBot[9].setGeometry(310+x, 460+y, 53, 38)
        self.stationsBot[10].setGeometry(525+x, 410+y, 53, 38)
        self.stationsBot[11].setGeometry(680+x, 290+y, 53, 38)
        self.stationsBot[12].setGeometry(770+x, 360+y, 53, 38)
        self.stationsBot[13].setGeometry(360+x, 287+y, 53, 38)
        self.stationsBot[14].setGeometry(300+x, 360+y, 53, 38)
        self.stationsBot[15].setGeometry(200+x, 270+y, 53, 38)
        self.stationsBot[16].setGeometry(290+x, 230+y, 53, 38)
        self.stationsBot[17].setGeometry(300+x, 135+y, 53, 38)

        self.stations[0].setGeometry(680+x, 32+y, 53, 38)
        self.stations[1].setGeometry(770+x, 100+y, 53, 38)
        self.stations[2].setGeometry(520+x, 75+y, 53, 38)
        self.stations[3].setGeometry(450+x, 75+y, 53, 38)
        self.stations[4].setGeometry(305+x, 32+y, 53, 38)
        self.stations[5].setGeometry(237+x, 32+y, 53, 38)
        self.stations[6].setGeometry(204+x, 100+y, 53, 38)
        self.stations[7].setGeometry(170+x, 32+y, 53, 38)
        self.stations[8].setGeometry(240+x, 460+y, 53, 38)
        self.stations[9].setGeometry(310+x, 460+y, 53, 38)
        self.stations[10].setGeometry(525+x, 410+y, 53, 38)
        self.stations[11].setGeometry(680+x, 290+y, 53, 38)
        self.stations[12].setGeometry(770+x, 360+y, 53, 38)
        self.stations[13].setGeometry(360+x, 287+y, 53, 38)
        self.stations[14].setGeometry(300+x, 360+y, 53, 38)
        self.stations[15].setGeometry(200+x, 270+y, 53, 38)
        self.stations[16].setGeometry(290+x, 230+y, 53, 38)
        self.stations[17].setGeometry(300+x, 135+y, 53, 38)
            

    # def make_beacons(self, tab1):
    #     original_pixmap_beacon = QPixmap("images/Beacon.png")
    #     resized_pixmap_beacon = original_pixmap_beacon.scaled(40,60)
    #     self.beacons = []
    #     self.beacons.append(QLabel(tab1))
    #     self.beacons[0].setPixmap(resized_pixmap_beacon)
    #     self.beacons[0].setGeometry(617, 30, 40, 60)

    #     self.beacons.append(QLabel(tab1))
    #     self.beacons[1].setPixmap(resized_pixmap_beacon)
    #     self.beacons[1].setGeometry(617, 221, 40, 60)

# Main entry to start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    upload_window = StartWindow()
    upload_window.show()
    sys.exit(app.exec())    