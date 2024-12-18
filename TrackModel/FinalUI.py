launcher = True
import sys
import requests
URL = 'http://127.0.0.1:5000'
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget, QLineEdit, QComboBox, QLabel, QTableView, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
if launcher:
    from TrackModel.TrackModel import buildTrack
    from TrackModel.Section import Section
    from TrackModel.Train import Train
    from TrackModel.Trains import Trains
    from TrackModel.TrafficLight import TrafficLight
    add_TM = "TrackModel/"
else:
    from TrackModel import buildTrack
    from Section import Section
    from Train import Train
    from Trains import Trains
    from TrafficLight import TrafficLight
    add_TM = ""

#Initialize all track global variables
redYard = [] 
redBlocks = []
redSwitches = []
redRailroadCrossings = []
redBeacons = [] 
redStations = [] 
redSections = []

greenYard = []
greenBlocks = [] 
greenSwitches = [] 
greenRailroadCrossings = []
greenTrafficLights = []
greenBeacons = []
greenStations = []
greenSections = []
#Initialize train global variables
trains = Trains()
#Initialize global occupation variables for Wayside
greenOccs = [False] * 151
redOccs = [False] * 77
#Initialize global variables for trains to recieve
auth = []
cmd = []

initialized = False

authAndSpeed = {
        'authorities' : None,
        'commandedSpeeds' : None
    }

numBoarding = {
        'num_boarding' : None,
        'id' : None
    }

class Bluh(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100, 100, 850, 550)
        self.setStyleSheet("background-color: grey")
        
        # Initialize variables to store input
        self.input_value1 = ""
        self.input_value2 = ""

        #Intialize start page widgets
        big_font = QFont("Arial", 14) # Create a font for labels and inputs
        self.label1 = QLabel("Red Track Excel Data", self) # Create labels
        self.label1.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label1.setFont(big_font)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label1.setGeometry(165, 100, 210, 40)
        self.label2 = QLabel("Green Track Excel Data", self)
        self.label2.setStyleSheet("background-color: #772CE8; color: black; border-radius: 10px;")  # Rounded corners
        self.label2.setFont(big_font)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align text
        self.label2.setGeometry(475, 100, 210, 40)
        self.text_entry1 = QLineEdit(self) # First text entry with custom position and size
        self.text_entry1.setFont(big_font)
        self.text_entry1.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry1.setPlaceholderText("Enter first value")
        self.text_entry1.setText("trackData/RedLine.xlsx")
        self.text_entry1.setGeometry(150, 150, 240, 40)
        self.text_entry2 = QLineEdit(self) # Second text entry with custom position and size
        self.text_entry2.setFont(big_font)
        self.text_entry2.setStyleSheet("background-color: #772CE8; color: black")
        self.text_entry2.setPlaceholderText("Enter second value")
        self.text_entry2.setText("trackData/GreenLine.xlsx")
        self.text_entry2.setGeometry(460, 150, 240, 40)
        self.button = QPushButton("Build Track", self) # Save button with custom position and size
        self.button.setStyleSheet("background-color: #772CE8; color: black")
        self.button.setFont(big_font)
        self.button.setGeometry(365, 240, 120, 50)
        self.button.clicked.connect(self.initialize_track)

    
    

#Main UI with maps, tables, test benches      
class TrackUI(QMainWindow):
    def __init__(self):
        super().__init__()
        global redYard, redBlocks, redSwitches, redRailroadCrossings, redBeacons, redStations, redSections
        global greenYard, greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations, greenSections
        self.initialize_track()
        
        #Make a PyQt Window
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100,100,850,550)
        self.setStyleSheet("background-color: grey")

        #Makes tabs for the windows
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.create_tabs()

        #Train movement function, called every ms
        self.train_timer = QTimer()
        self.train_timer.timeout.connect(trains.get_info)
        self.train_timer.start(10)

        self.send_timer = QTimer()
        self.send_timer.timeout.connect(self.post_auth_and_cmd_speed)
        self.send_timer.start(1000)

    def initialize_track(self):
        global initialized 
        initialized = True
        global redYard, redBlocks, redSwitches, redRailroadCrossings, redBeacons, redStations, redSections
        global greenYard, greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations, greenSections
        global trains
        # Store text entry values in separate variables
        self.input_value1 = "trackData/RedLine.xlsx"
        self.input_value2 = "trackData/GreenLine.xlsx"

        #Red Line initial prep
        redBlocks, redSwitches, redRailroadCrossings, redBeacons, redStations = buildTrack(add_TM+self.input_value1)

        redSections = [] # Make red sections
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
        redSections.append(Section('Yard'))

        for i in range(76): #Place blocks in sections
            if i == 0:
                redSections[10].add_block(redBlocks[i])
            elif i >= 1 and i < 10:
                redSections[0].add_block(redBlocks[i])
            elif i >= 10 and i < 16:
                redSections[1].add_block(redBlocks[i])
            elif i >= 16 and i < 28:
                redSections[2].add_block(redBlocks[i])
            elif i >= 28 and i < 33:
                redSections[3].add_block(redBlocks[i])
            elif i >= 33 and i < 39:
                redSections[4].add_block(redBlocks[i])
            elif i >= 39 and i < 44:
                redSections[5].add_block(redBlocks[i])
            elif i >= 44 and i < 53:
                redSections[6].add_block(redBlocks[i])
            elif i >= 53 and i < 67:
                redSections[7].add_block(redBlocks[i])
            elif i >= 67 and i < 72:
                redSections[8].add_block(redBlocks[i])
            elif i >= 72 and i < 77:
                redSections[9].add_block(redBlocks[i])
            
        greenBlocks, greenSwitches, greenRailroadCrossings, greenBeacons, greenStations = buildTrack(add_TM+self.input_value2)
        
        for i in range(10):
            greenTrafficLights.append(TrafficLight("Green", False))

        #override for sake of spawn simulation
        for i in range(150):
            greenBlocks[i].set_cmd_speed(greenBlocks[i].speedLimit)
        #greenBlocks[85].set_authority(262.7)
        
        greenSections = [] # make green sections
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
        greenSections.append(Section('Yard'))
        for i in range(150): #Place blocks in sections
            if i == 0:
                greenSections[10].add_block(greenBlocks[i])
            elif i >= 1 and i < 13:
                greenSections[0].add_block(greenBlocks[i])
            elif i >= 13 and i < 29:
                greenSections[1].add_block(greenBlocks[i])
            elif i >= 29 and i < 58:
                greenSections[2].add_block(greenBlocks[i])
            elif i >= 58 and i < 63:
                greenSections[3].add_block(greenBlocks[i])
            elif i >= 63 and i < 77:
                greenSections[4].add_block(greenBlocks[i])
            elif i >= 77 and i < 86:
                greenSections[5].add_block(greenBlocks[i])
            elif i >= 86 and i < 101:
                greenSections[6].add_block(greenBlocks[i])
            elif i >= 101 and i < 118:
                greenSections[7].add_block(greenBlocks[i])
            elif i >= 118 and i < 136:        
                greenSections[8].add_block(greenBlocks[i])
            elif i >= 136 and i < 151:
                greenSections[9].add_block(greenBlocks[i])   
        
            
        #Train (temporary until we figure out how to initialize a train)
        # tempTrain = Train(10, greenBlocks[0], 32.2, 0, "Green")
        # trains.addTrain(tempTrain)
        # auth.append(0.0)
        # cmd.append(0.0)
    
    #For Wayside
    def get_occupancies(self):
        occ_data = {"Green" : greenOccs,
                    "Red" : redOccs}
        return occ_data

    #For Train Model
    def get_track_to_train(self):
        for i in range(len(Trains)):
            auth[i] = Trains[i].trainAuth
            cmd[i] = Trains[i].trainCmd
        data = { "authority" : auth, 
                 "commandedSpeed" : cmd}
        return data
    
    #From Wayside
    def set_signals(self, data):
        if initialized == False:
            return
        
        for switch in data['Green']['switches']:
            switch_id = switch['id']
            if switch['toggled'] == 0:
                greenSwitches[switch_id].set_L()
            else:
                greenSwitches[switch_id].set_R()
        for traffic in data['Green']['traffic_lights']:
            traffic_id = traffic['id']
            if traffic['toggled'] == 0:
                greenTrafficLights[traffic_id].set_R()
            else:
                greenTrafficLights[traffic_id].set_G()
        for crossing in data['Green']['crossings']:   
            crossing_id = crossing['id']
            if crossing['toggled'] == 0:
                greenRailroadCrossings[crossing_id].set_U()
            else:
                greenRailroadCrossings[crossing_id].set_D()

        for switch in data['Red']['switches']:
            switch_id = switch['id']
            if switch['toggled'] == 0:
                redSwitches[switch_id].set_L()
            else:
                redSwitches[switch_id].set_R()
        for traffic in data['Red']['traffic_lights']:
            traffic_id = traffic['id']
            #if traffic['toggled'] == 0:
                #redTrafficLights[traffic_id].set_R()
            #else:
                #redTrafficLights[traffic_id].set_G()
        for crossing in data['Red']['crossings']:   
            crossing_id = crossing['id']
            if crossing['toggled'] == 0:
                redRailroadCrossings[crossing_id].set_U()
            else:
                redRailroadCrossings[crossing_id].set_D()

    def set_maintenance(self, data):
        print(data)
        if data['line'] == 'Green':
            greenBlocks[data['index']].set_closed(data['maintenance'])
        elif data['line'] == 'Red':
            redBlocks[data['index']].set_closed(data['maintenance'])

    def set_block_authority(self, data):
        if data['line'] == 'Green':
            greenBlocks[data['index']].set_authority(data['authority'])
        elif data['line'] == 'Red':
            redBlocks[data['index']].set_authority(data['authority'])

    def set_block_cmdSpeed(self, data):
        if data['line'] == 'Green':
            greenBlocks[data['index']].set_cmd_speed(data['speed'])
        elif data['line'] == 'Red':
            redBlocks[data['index']].set_cmd_speed(data['speed'])

    def set_indexed_train_auth_diff(self,index,diff):
        if initialized == False:
            return
        trains.trainList[index].moveTrain(diff)

    def post_people_boarding(self, numLeaving, index):
        numBoarding['num_boarding'] = trains.trainList[index].station_stopped(numLeaving)
        numBoarding['id'] = index
        print(f"Index{index}")
        print(f"Number leaving: {trains.trainList[index].station_stopped(numLeaving)}")
        if launcher:
            response = requests.post(URL + "/train-model/get-data/station_passengers", json = numBoarding)


    def post_auth_and_cmd_speed(self):
        authAndSpeed["authorities"]=trains.authorities
        authAndSpeed["commandedSpeeds"]=trains.commandedSpeeds
        if launcher:
            response = requests.post(URL + "/train-model/get-data/authority-cmd-speed", json=authAndSpeed)

    def make_train(self, line):
        if (line == "Green"):
            tempTrain = Train(10, greenBlocks[0], 32.2, len(trains.trainList), line)
        elif (line == "Red"):
            tempTrain = Train(10, redBlocks[0], 32.2, len(trains.trainList), line)
        trains.addTrain(tempTrain)
        auth.append(0.0)
        cmd.append(0.0)

    #initializes all maps, tables, test benches
    def create_tabs(self):
        #Tab 3 for green line
        tab1 = QWidget()
        self.tab_widget.addTab(tab1, "Green Line")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_green_sections(tab1, -100, 50)
        self.make_green_switches(tab1, -100, 50)
        self.make_green_crossings(tab1, 0, 0)
        self.make_green_stations(tab1, 0, 0)
        self.make_green_lights(tab1, 0)
        self.make_green_failure_buttons(tab1)
        self.make_green_temp(tab1)
    
        #Tab 5 for table info 
        tab2 = QWidget()
        self.tab_widget.addTab(tab2, "Green Track Info")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_green_track_table(tab2)

        #Tab 4 for test bench
        #input track changes here
        tab4 = QWidget()
        self.tab_widget.addTab(tab4, "Green Test Bench")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_green_test_bench(tab4, -30)

        tab3 = QWidget()
        self.tab_widget.addTab(tab3, "Train Info")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_train_table(tab3)

        #Create Tab 1 red line
        tab5 = QWidget()
        self.tab_widget.addTab(tab5, "Red Line")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_red_sections(tab5)
        self.make_red_switches(tab5)
        # self.make_lights(tab1, 110)
        self.make_red_crossings(tab5)
        # self.make_train(tab1)
        self.make_red_stations(tab5)
        self.make_red_temp(tab5)
        self.make_red_failure_buttons(tab5)

        #Tab 2 for table info 
        tab6 = QWidget()
        self.tab_widget.addTab(tab6, "Red Track Info")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_red_track_table(tab6)



        #Tab 3 for test bench
        #input track changes here
        tab8 = QWidget()
        self.tab_widget.addTab(tab8, "Red Test Bench")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")
        
        self.make_red_test_bench(tab8, -30)

    #initializes red line table
    def make_red_track_table(self, tab):
        self.red_block_table = QStandardItemModel(len(redBlocks), 15)
        self.red_block_table.setHorizontalHeaderLabels(["Block", "Occupied", "Authority", "Cmd. Speed", "Beacon", "Station", "Railroad", "Switch", "Traffic Light", "Next Block", "Previous Block", "Length", "Grade", "Speed Limit", "Elevation", "Cum. Elevation", "Underground", "Broken Track", "Circuit Failure", "Power Failure"])
        self.populate_red_track_table()

        red_block_table_view = QTableView()
        red_block_table_view.setModel(self.red_block_table)

        layout = QVBoxLayout()
        layout.addWidget(red_block_table_view)
        tab.setLayout(layout)

    #red table update function
    def populate_red_track_table(self):
        for row in range(len(redBlocks)):
            for col in range(20):
                value = redBlocks[row].get_table_data(col)
                item = QStandardItem(value)
                self.red_block_table.setItem(row, col, item)
                item.setBackground(Qt.GlobalColor.darkGray)
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
                
    #initialize green line table
    def make_green_track_table(self, tab):
        self.green_block_table = QStandardItemModel(len(greenBlocks), 18)
        self.green_block_table.setHorizontalHeaderLabels(["Number", "Occupied", "Authority", "Commanded Speed", "Beacon", "Station", "Railroad", "Switch", "Next Block", "Previous Block", "Length", "Grade", "Speed Limit", "Elevation", "Cum. Elevation", "Underground", "Broken Track", "Circuit Failure", "Power Failure"])
        self.populate_green_track_table()

        green_block_table_view = QTableView()
        green_block_table_view.setModel(self.green_block_table)
        
        layout = QVBoxLayout()
        layout.addWidget(green_block_table_view)
        tab.setLayout(layout)

    def make_train_table(self, tab):
        self.green_train_table = QStandardItemModel(len(trains.trainList), 8)
        self.green_train_table.setHorizontalHeaderLabels(["ID", "Cmd. Speed", "Authority", "Commanded Speed", "Front Block", "Location", "Back Block", "Location"])
        self.populate_train_table()

        green_train_table_view = QTableView()
        green_train_table_view.setModel(self.green_train_table)

        layout = QVBoxLayout()
        layout.addWidget(green_train_table_view)
        tab.setLayout(layout)
    
    #green table update function
    def populate_green_track_table(self):
        for row in range(len(greenBlocks)):
            for col in range(18):
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

    def populate_train_table(self):
        # Ensure the table has the correct number of rows
        current_row_count = self.green_train_table.rowCount()
        required_row_count = len(trains.trainList)
        
        # Add rows if trainList has grown
        if required_row_count > current_row_count:
            for _ in range(required_row_count - current_row_count):
                self.green_train_table.appendRow([QStandardItem("") for _ in range(8)])

        # Populate the table with data
        for row in range(required_row_count):
            for col in range(8):
                value = trains.trainList[row].get_table_data(col)
                item = QStandardItem(value)
                self.green_train_table.setItem(row, col, item)
                item.setBackground(Qt.GlobalColor.darkGray)

    #red map update function         
    def update_red_ui(self):
        self.populate_red_track_table()
        self.populate_train_table()
        #All "setToolTip" functions are updating the hover information for all objects
        #Constantly update block color based on occupied variable
        for i in range(11):
            #if occupied hide blue arrow, white is underneath
            redSections[i].check_occupied()
            if redSections[i].get_occupied():
                self.redArrows[i].hide()
            else:
                self.redArrows[i].show()
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
            self.leftRedSwitches[i].setToolTip(redSwitches[i].display_info(i))
            self.rightRedSwitches[i].setToolTip(redSwitches[i].display_info(i))

        for i in range(8):
            if redStations[i].get_trainIn():
                self.redStationsTop[i].hide()
            else:
                self.redStationsTop[i].show()
            self.redStationsBot[i].setToolTip(redStations[i].display_info())
            self.redStationsTop[i].setToolTip(redStations[i].display_info())

        for i in range(2):
            if greenRailroadCrossings[i].get_UorD():
                self.redGreenCrossings[i].hide()
            else:
                self.redGreenCrossings[i].show()
            self.redGreenCrossings[i].setToolTip(redRailroadCrossings[i].display_info(i))
            self.redRedCrossings[i].setToolTip(redRailroadCrossings[i].display_info(i))


    

    #green map update function
    def update_green_ui(self):
        self.populate_green_track_table()
        
        for i in range(150):
            greenBlocks[i].set_occupancies()
            greenOccs[i] = greenBlocks[i].occupancy
        #All "setToolTip" functions are updating the hover information for all objects
        #Constantly update block color based on occupied variable
        for i in range(11):
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
            self.leftGreenSwitches[i].setToolTip(greenSwitches[i].display_info(i))
            self.rightGreenSwitches[i].setToolTip(greenSwitches[i].display_info(i))

        # #Constantly update traffic light color based on red or green variable
        for i in range(10):
            #red is underneath green
            if greenTrafficLights[i].get_RorG():
                self.greenLightsTop[i].show()
            else:
                self.greenLightsTop[i].hide()
            self.greenLightsTop[i].setToolTip(greenTrafficLights[i].display_info(i))
            self.greenLightsBot[i].setToolTip(greenTrafficLights[i].display_info(i))
            
        #Constantly update railroad crossing color based on up or down variable
        for i in range(2):
            if greenRailroadCrossings[i].get_UorD():
                self.greenGreenCrossings[i].hide()
            else:
                self.greenGreenCrossings[i].show()
            self.greenGreenCrossings[i].setToolTip(greenRailroadCrossings[i].display_info(i))
            self.greenRedCrossings[i].setToolTip(greenRailroadCrossings[i].display_info(i))

        #self.trainLabel.setToolTip(trains.trainList[0].display_info(0))

        for i in range(18):
            if greenStations[i].get_trainIn():
                self.greenStationsTop[i].hide()
            else:
                self.greenStationsTop[i].show()
            self.greenStationsBot[i].setToolTip(greenStations[i].display_info())
            self.greenStationsTop[i].setToolTip(greenStations[i].display_info())

        # self.beacons[0].setToolTip(blueBeacons[0].display_info())
        # self.beacons[1].setToolTip(blueBeacons[1].display_info())

    #initialize red test bench
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

    #update red test bench
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
                    redRailroadCrossings[id].set_U()
                else:
                    redRailroadCrossings[id].set_D()
            else:
                print("Index Error sendButton_click function.")
        #if row 3 input for traffic lights
        # elif i == 2:
        #     if id <= 10 and id >= 0:
        #         if var == "Red":
        #             redTrafficLights[id].set_R()
        #         else:
        #             redTrafficLights[id].set_G()
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
                    redBlocks[id].set_O()
                else:
                    redBlocks[id].set_N()
            else:
                print("Index Error sendButton_click function.")

    #initialize green test bench
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

    #update green test bench
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
            if id <= 5 and id >= 0:
                if var == "Red":
                    greenTrafficLights[id].set_R()
                else:
                    greenTrafficLights[id].set_G()
            else:
                print("Index Error sendButton_click function.")
        #if row 4 input authority for specific block changes
        elif i == 3:
            if id <= 150 and id >= 1:
                greenBlocks[id].set_authority(float(var))
            else:
                print("Index Error")
        #if row 5 input commanded speed for specific block changes
        elif i == 4:
            if id <= 150 and id >= 1:
                greenBlocks[id].set_cmd_speed(float(var))
            else:
                print("Index Error sendButton_click function.")
        #if row 6 input change a blocks occupancy
        elif i == 5:
            if id <= 150 and id >= 1:
                if var == "Occupied":
                    greenBlocks[id].set_O()
                else:
                    greenBlocks[id].set_N()
            else:
                print("Index Error sendButton_click function.")

    #initializes green failure mode buttons
    def make_green_failure_buttons(self, tab1):
        self.greenFailureButtons = []
        failureText = ['Broken Track', 'Track Circuit Failure', 'Power Failure']
        for i in range(3):
            self.greenFailureButtons.append(QPushButton(failureText[i], tab1))
            self.greenFailureButtons[i].setStyleSheet("background-color: white; color: black;")
            self.greenFailureButtons[i].clicked.connect(lambda _, index=i: self.send_green_failure_button_click(index))
            self.greenFailureButtons[i].setGeometry(20, 410 + 30 * i, 120, 25)  

        self.blockNum = QLineEdit(tab1)
        self.blockNum.setStyleSheet("background-color: white; color: black;")
        self.blockNum.setGeometry(20, 380, 70, 25)

        self.blockLabel = QLabel('Block Number:', tab1)
        self.blockLabel.setStyleSheet("color: white;")
        self.blockLabel.setGeometry(20, 360, 100, 20)

    def make_red_failure_buttons(self, tab1):
        self.redFailureButtons = []
        failureText = ['Broken Track', 'Track Circuit Failure', 'Power Failure']
        for i in range(3):
            self.redFailureButtons.append(QPushButton(failureText[i], tab1))
            self.redFailureButtons[i].setStyleSheet("background-color: white; color: black;")
            self.redFailureButtons[i].clicked.connect(lambda _, index=i: self.send_red_failure_button_click(index))
            self.redFailureButtons[i].setGeometry(20, 410 + 30 * i, 120, 25)  

        self.blockNum = QLineEdit(tab1)
        self.blockNum.setStyleSheet("background-color: white; color: black;")
        self.blockNum.setGeometry(20, 380, 70, 25)

        self.blockLabel = QLabel('Block Number:', tab1)
        self.blockLabel.setStyleSheet("color: white;")
        self.blockLabel.setGeometry(20, 360, 100, 20)


    #update green failure modes    
    def send_green_failure_button_click(self, i): 
        num = int(self.blockNum.text()) 
        if num >= 1 and num <= 150:    
            if i == 0:
                greenBlocks[num].change_broken()
            elif i == 1:
                greenBlocks[num].change_circuit()
            elif i == 2:
                greenBlocks[num].change_power()

    #update green failure modes    
    def send_red_failure_button_click(self, i): 
        num = int(self.blockNum.text()) 
        if num >= 1 and num <= 76:    
            if i == 0:
                redBlocks[num].change_broken()
            elif i == 1:
                redBlocks[num].change_circuit()
            elif i == 2:
                redBlocks[num].change_power()

    #initialize red section map features
    def make_red_sections(self, tab1):
        #White arrows are behind blue arrows so you can show or hide the blue arrows
        self.underRedArrows = []
        self.redArrows = []
        original_pixmap_white = QPixmap(add_TM+"images/WhiteFlatArrow.png")
        resized_pixmap_white = original_pixmap_white.scaled(60,30)
        original_pixmap_blue = QPixmap(add_TM+"images/RedFlatArrow.png")
        resized_pixmap_blue = original_pixmap_blue.scaled(60,30)
        original_tester = QPixmap(add_TM+"images/SizeTester.png")
        section0_top = QPixmap(add_TM+"images/RedSection0Top.png")
        section0_top = section0_top.scaled(114,30)
        section0_bot = QPixmap(add_TM+"images/RedSection0Bot.png")
        section0_bot = section0_bot.scaled(114,30)
        section2_top = QPixmap(add_TM+"images/RedSection2Top.png")
        section2_top = section2_top.scaled(168,30)
        section2_bot = QPixmap(add_TM+"images/RedSection2Bot.png")
        section2_bot = section2_bot.scaled(168,30)
        section3_top = QPixmap(add_TM+"images/RedSection3Top.png")
        section3_top = section3_top.scaled(50,30)
        section3_bot = QPixmap(add_TM+"images/RedSection3Bot.png")
        section3_bot = section3_bot.scaled(50,30)
        section4_top = QPixmap(add_TM+"images/RedSection4Top.png")
        section4_top = section4_top.scaled(60,245)
        section4_bot = QPixmap(add_TM+"images/RedSection4Bot.png")
        section4_bot = section4_bot.scaled(60,245)
        section7_top = QPixmap(add_TM+"images/RedSection7Top.png")
        section7_top = section7_top.scaled(107,123)
        section7_bot = QPixmap(add_TM+"images/RedSection7Bot.png")
        section7_bot = section7_bot.scaled(107,123)
        redYard_top = QPixmap(add_TM+"images/RedYardTop.png")
        redYard_top = redYard_top.scaled(100,40)
        redYard_bot = QPixmap(add_TM+"images/YardBot.png")
        redYard_bot = redYard_bot.scaled(100,40)
        for i in range(11):
            self.underRedArrows.append(QLabel(tab1))
            self.underRedArrows[i].setPixmap(resized_pixmap_white)
            
            self.redArrows.append(QLabel(tab1))
            self.redArrows[i].setPixmap(resized_pixmap_blue)

        self.redArrows[0].setPixmap(section0_top)
        self.underRedArrows[0].setPixmap(section0_bot)
        self.redArrows[1].setPixmap(section0_top)
        self.underRedArrows[1].setPixmap(section0_bot)
        self.redArrows[2].setPixmap(section2_top)
        self.underRedArrows[2].setPixmap(section2_bot)
        self.redArrows[6].setPixmap(section2_top)
        self.underRedArrows[6].setPixmap(section2_bot)
        self.redArrows[3].setPixmap(section3_top)
        self.underRedArrows[3].setPixmap(section3_bot)
        self.redArrows[5].setPixmap(section3_top)
        self.underRedArrows[5].setPixmap(section3_bot)
        self.redArrows[7].setPixmap(section7_top)
        self.underRedArrows[7].setPixmap(section7_bot)
        self.redArrows[8].setPixmap(section3_top)
        self.underRedArrows[8].setPixmap(section3_bot)
        self.redArrows[9].setPixmap(section3_top)
        self.underRedArrows[9].setPixmap(section3_bot)
        self.redArrows[4].setPixmap(section4_top)
        self.underRedArrows[4].setPixmap(section4_bot)
        

        self.underRedArrows[0].setGeometry(134, 77, 114, 30)
        self.redArrows[0].setGeometry(134, 77, 114, 30)
        self.underRedArrows[1].setGeometry(134, 180, 114, 30)
        self.redArrows[1].setGeometry(134, 180, 114, 30)
        self.underRedArrows[2].setGeometry(331, 127, 168, 30)
        self.redArrows[2].setGeometry(331, 127, 168, 30)
        self.underRedArrows[3].setGeometry(582, 77, 50, 30)
        self.redArrows[3].setGeometry(582, 77, 50, 30)
        self.underRedArrows[4].setGeometry(715, 131, 60, 245)
        self.redArrows[4].setGeometry(715, 131, 60, 245)
        self.underRedArrows[5].setGeometry(582, 400, 50, 30)
        self.redArrows[5].setGeometry(582, 400, 50, 30)
        self.underRedArrows[6].setGeometry(331, 346, 168, 30)
        self.redArrows[6].setGeometry(331, 346, 168, 30)
        self.underRedArrows[7].setGeometry(143, 300, 107, 123)
        self.redArrows[7].setGeometry(143, 300, 107, 123)
        self.underRedArrows[8].setGeometry(582, 297, 50, 30)
        self.redArrows[8].setGeometry(582, 297, 50, 30)
        self.underRedArrows[9].setGeometry(582, 177, 50, 30)
        self.redArrows[9].setGeometry(582, 177, 50, 30)

        self.redArrows[10].setPixmap(redYard_top)
        self.underRedArrows[10].setPixmap(redYard_bot) 
        self.redArrows[10].setGeometry(20, 220, 100, 40) 
        self.underRedArrows[10].setGeometry(20, 220, 100, 40)
        

        #this is the timer that constantly updates the states for all of the components 
        self.red_timer = QTimer()
        self.red_timer.timeout.connect(self.update_red_ui)
        self.red_timer.start(100)

    #initialize green section map features
    def make_green_sections(self, tab3, x, y):
        #White arrows are behind blue arrows so you can show or hide the blue arrows
        self.underGreenArrows = []
        self.greenArrows = []
        original_pixmap_white = QPixmap(add_TM+"images/WhiteFlatArrow.png")
        resized_pixmap_white = original_pixmap_white.scaled(60,30)
        original_pixmap_green = QPixmap(add_TM+"images/GreenFlatArrow.png")
        resized_pixmap_green = original_pixmap_green.scaled(60,30)
        original_tester = QPixmap(add_TM+"images/SizeTester.png")
        section0_top = QPixmap(add_TM+"images/GreenSection0Top.png")
        section0_top = section0_top.scaled(107,123)
        section0_bot = QPixmap(add_TM+"images/GreenSection0Bot.png")
        section0_bot = section0_bot.scaled(107,123)
        section1_top = QPixmap(add_TM+"images/GreenSection1Top.png")
        section1_top = section1_top.scaled(129,30)
        section1_bot = QPixmap(add_TM+"images/GreenSection1Bot.png")
        section1_bot = section1_bot.scaled(129,30)
        section2_top = QPixmap(add_TM+"images/GreenSection2Top.png")
        section2_top = section2_top.scaled(213,30)
        section2_bot = QPixmap(add_TM+"images/GreenSection2Bot.png")
        section2_bot = section2_bot.scaled(213,30)
        section3_top = QPixmap(add_TM+"images/GreenSection3Top.png")
        section3_top = section3_top.scaled(30,183)
        section3_bot = QPixmap(add_TM+"images/GreenSection3Bot.png")
        section3_bot = section3_bot.scaled(30,183)
        section4_top = QPixmap(add_TM+"images/GreenSection4Top.png")
        section4_top = section4_top.scaled(207,30)
        section4_bot = QPixmap(add_TM+"images/GreenSection4Bot.png")
        section4_bot = section4_bot.scaled(207,30)
        section5_top = QPixmap(add_TM+"images/GreenSection5Top.png")
        section5_top = section5_top.scaled(57,30)
        section5_bot = QPixmap(add_TM+"images/GreenSection5Bot.png")
        section5_bot = section5_bot.scaled(57,30)
        section6_top = QPixmap(add_TM+"images/GreenSection0Top.png")
        section6_top = section6_top.scaled(107,123)
        section6_bot = QPixmap(add_TM+"images/GreenSection0Bot.png")
        section6_bot = section6_bot.scaled(107,123)
        section7_top = QPixmap(add_TM+"images/GreenSection7Top.png")
        section7_top = section7_top.scaled(149, 30)
        section7_bot = QPixmap(add_TM+"images/GreenSection7Bot.png")
        section7_bot = section7_bot.scaled(149, 30)
        section8_top = QPixmap(add_TM+"images/GreenSection8Top.png")
        section8_top = section8_top.scaled(30,156)
        section8_bot = QPixmap(add_TM+"images/GreenSection8Bot.png")
        section8_bot = section8_bot.scaled(30,156)
        section9_top = QPixmap(add_TM+"images/GreenSection9Top.png")
        section9_top = section9_top.scaled(103,30)
        section9_bot = QPixmap(add_TM+"images/GreenSection9Bot.png")
        section9_bot = section9_bot.scaled(103,30)
        greenYard_top = QPixmap(add_TM+"images/GreenYardTop.png")
        greenYard_top = greenYard_top.scaled(100,40)
        greenYard_bot = QPixmap(add_TM+"images/YardBot.png")
        greenYard_bot = greenYard_bot.scaled(100,40)
        for i in range(11):
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

        self.greenArrows[10].setPixmap(greenYard_top)
        self.underGreenArrows[10].setPixmap(greenYard_bot)  
        self.underGreenArrows[10].setGeometry(120+x, 200+y, 100, 40)
        self.greenArrows[10].setGeometry(120+x, 200+y, 100, 40)

        #this is the timer that constantly updates the states for all of the components 
        self.green_timer = QTimer()
        self.green_timer.timeout.connect(self.update_green_ui)
        self.green_timer.start(100)

    #initialize red switch map features
    def make_red_switches(self, tab3):
        self.leftRedSwitches = []
        self.rightRedSwitches = []
        original_pixmap_left = QPixmap(add_TM+"images/SwitchLeft.png")
        resized_pixmap_left = original_pixmap_left.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right = QPixmap(add_TM+"images/SwitchRight.png")
        resized_pixmap_right = original_pixmap_right.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_reversed = QPixmap(add_TM+"images/SwitchLeftReversed.png")
        resized_pixmap_left_reversed = original_pixmap_left_reversed.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_reversed = QPixmap(add_TM+"images/SwitchRightReversed.png")
        resized_pixmap_right_reversed = original_pixmap_right_reversed.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_red1 = QPixmap(add_TM+"images/SwitchLeftRed1.png")
        resized_pixmap_left_red1 = original_pixmap_left_red1.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_red1 = QPixmap(add_TM+"images/SwitchRightRed1.png")
        resized_pixmap_right_red1 = original_pixmap_right_red1.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[0].setPixmap(resized_pixmap_right_red1)
        self.leftRedSwitches[0].setGeometry(50, 80, 83, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[0].setPixmap(resized_pixmap_left_red1)
        self.rightRedSwitches[0].setGeometry(50, 80, 83, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[1].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[1].setGeometry(250, 80, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[1].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[1].setGeometry(250, 80, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[2].setPixmap(resized_pixmap_left)
        self.leftRedSwitches[2].setGeometry(500, 80, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[2].setPixmap(resized_pixmap_right)
        self.rightRedSwitches[2].setGeometry(500, 80, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[3].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[3].setGeometry(633, 80, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[3].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[3].setGeometry(633, 80, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[4].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[4].setGeometry(633, 300, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[4].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[4].setGeometry(633, 300, 80, 125)

        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[5].setPixmap(resized_pixmap_left)
        self.leftRedSwitches[5].setGeometry(500, 300, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[5].setPixmap(resized_pixmap_right)
        self.rightRedSwitches[5].setGeometry(500, 300, 80, 125)
        
        self.leftRedSwitches.append(QLabel(tab3))
        self.leftRedSwitches[6].setPixmap(resized_pixmap_left_reversed)
        self.leftRedSwitches[6].setGeometry(250, 300, 80, 125)
        self.rightRedSwitches.append(QLabel(tab3))
        self.rightRedSwitches[6].setPixmap(resized_pixmap_right_reversed)
        self.rightRedSwitches[6].setGeometry(250, 300, 80, 125)

    #initialize green switch map features
    def make_green_switches(self, tab3, x, y):
        self.leftGreenSwitches = []
        self.rightGreenSwitches = []
        original_pixmap_left = QPixmap(add_TM+"images/SwitchLeft.png")
        resized_pixmap_left = original_pixmap_left.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right = QPixmap(add_TM+"images/SwitchRight.png")
        resized_pixmap_right = original_pixmap_right.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_reversed = QPixmap(add_TM+"images/SwitchLeftReversed.png")
        resized_pixmap_left_reversed = original_pixmap_left_reversed.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_reversed = QPixmap(add_TM+"images/SwitchRightReversed.png")
        resized_pixmap_right_reversed = original_pixmap_right_reversed.scaled(80,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

        original_pixmap_left_red1 = QPixmap(add_TM+"images/SwitchLeftRed1.png")
        resized_pixmap_left_red1 = original_pixmap_left_red1.scaled(83,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        original_pixmap_right_red1 = QPixmap(add_TM+"images/SwitchRightRed1.png")
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

    #initialize green crossing map features
    def make_green_crossings(self, tab3, x, y):
        original_pixmap_red = QPixmap(add_TM+"images/RedCrossing.png")
        resized_pixmap_red = original_pixmap_red.scaled(50,50)
        original_pixmap_green = QPixmap(add_TM+"images/GreenCrossing.png")
        resized_pixmap_green = original_pixmap_green.scaled(50,50)
        self.greenRedCrossings = []
        self.greenGreenCrossings = []

        self.greenRedCrossings.append(QLabel(tab3))
        self.greenRedCrossings[0].setPixmap(resized_pixmap_red)
        self.greenRedCrossings[0].setGeometry(490, 145, 50, 50)
        self.greenGreenCrossings.append(QLabel(tab3))
        self.greenGreenCrossings[0].setPixmap(resized_pixmap_green)
        self.greenGreenCrossings[0].setGeometry(490, 145, 50, 50)

        self.greenRedCrossings.append(QLabel(tab3))
        self.greenRedCrossings[1].setPixmap(resized_pixmap_red)
        self.greenRedCrossings[1].setGeometry(310, 280, 50, 50)
        self.greenGreenCrossings.append(QLabel(tab3))
        self.greenGreenCrossings[1].setPixmap(resized_pixmap_green)
        self.greenGreenCrossings[1].setGeometry(310, 280, 50, 50)

    def make_red_crossings(self, tab3):
        original_pixmap_red = QPixmap(add_TM+"images/RedCrossing.png")
        resized_pixmap_red = original_pixmap_red.scaled(50,50)
        original_pixmap_green = QPixmap(add_TM+"images/GreenCrossing.png")
        resized_pixmap_green = original_pixmap_green.scaled(50,50)
        self.redRedCrossings = []
        self.redGreenCrossings = []

        self.redRedCrossings.append(QLabel(tab3))
        self.redRedCrossings[0].setPixmap(resized_pixmap_red)
        self.redRedCrossings[0].setGeometry(165, 210, 50, 50)
        self.redGreenCrossings.append(QLabel(tab3))
        self.redGreenCrossings[0].setPixmap(resized_pixmap_green)
        self.redGreenCrossings[0].setGeometry(165, 210, 50, 50)

        self.redRedCrossings.append(QLabel(tab3))
        self.redRedCrossings[1].setPixmap(resized_pixmap_red)
        self.redRedCrossings[1].setGeometry(382, 375, 50, 50)
        self.redGreenCrossings.append(QLabel(tab3))
        self.redGreenCrossings[1].setPixmap(resized_pixmap_green)
        self.redGreenCrossings[1].setGeometry(382, 375, 50, 50)
    
    #initialize green station map features
    def make_green_stations(self,tab1,x, y):
        original_pixmap_station = QPixmap(add_TM+"images/Station.png")
        resized_pixmap_station = original_pixmap_station.scaled(53,38)
        original_pixmap_station_bot = QPixmap(add_TM+"images/StationBot.png")
        resized_pixmap_station_bot = original_pixmap_station_bot.scaled(53,38)
        self.greenStationsTop = []
        self.greenStationsBot = []
        for i in range(18):
            self.greenStationsBot.append(QLabel(tab1))
            self.greenStationsBot[i].setPixmap(resized_pixmap_station_bot)
            self.greenStationsTop.append(QLabel(tab1))
            self.greenStationsTop[i].setPixmap(resized_pixmap_station)
        self.greenStationsBot[0].setGeometry(680+x, 197+y, 53, 38)
        self.greenStationsBot[1].setGeometry(770+x, 100+y, 53, 38)
        self.greenStationsBot[2].setGeometry(520+x, 75+y, 53, 38)
        self.greenStationsBot[3].setGeometry(450+x, 75+y, 53, 38)
        self.greenStationsBot[4].setGeometry(305+x, 32+y, 53, 38)
        self.greenStationsBot[5].setGeometry(237+x, 32+y, 53, 38)
        self.greenStationsBot[6].setGeometry(204+x, 100+y, 53, 38)
        self.greenStationsBot[7].setGeometry(170+x, 32+y, 53, 38)
        self.greenStationsBot[8].setGeometry(240+x, 460+y, 53, 38)
        self.greenStationsBot[9].setGeometry(310+x, 460+y, 53, 38)
        self.greenStationsBot[10].setGeometry(525+x, 410+y, 53, 38)
        self.greenStationsBot[11].setGeometry(680+x, 290+y, 53, 38)
        self.greenStationsBot[12].setGeometry(770+x, 360+y, 53, 38)
        self.greenStationsBot[13].setGeometry(360+x, 287+y, 53, 38)
        self.greenStationsBot[14].setGeometry(300+x, 360+y, 53, 38)
        self.greenStationsBot[15].setGeometry(200+x, 270+y, 53, 38)
        self.greenStationsBot[16].setGeometry(290+x, 230+y, 53, 38)
        self.greenStationsBot[17].setGeometry(300+x, 135+y, 53, 38)

        self.greenStationsTop[0].setGeometry(680+x, 197+y, 53, 38)
        self.greenStationsTop[1].setGeometry(770+x, 100+y, 53, 38)
        self.greenStationsTop[2].setGeometry(520+x, 75+y, 53, 38)
        self.greenStationsTop[3].setGeometry(450+x, 75+y, 53, 38)
        self.greenStationsTop[4].setGeometry(305+x, 32+y, 53, 38)
        self.greenStationsTop[5].setGeometry(237+x, 32+y, 53, 38)
        self.greenStationsTop[6].setGeometry(204+x, 100+y, 53, 38)
        self.greenStationsTop[7].setGeometry(170+x, 32+y, 53, 38)
        self.greenStationsTop[8].setGeometry(240+x, 460+y, 53, 38)
        self.greenStationsTop[9].setGeometry(310+x, 460+y, 53, 38)
        self.greenStationsTop[10].setGeometry(525+x, 410+y, 53, 38)
        self.greenStationsTop[11].setGeometry(680+x, 290+y, 53, 38)
        self.greenStationsTop[12].setGeometry(770+x, 360+y, 53, 38)
        self.greenStationsTop[13].setGeometry(360+x, 287+y, 53, 38)
        self.greenStationsTop[14].setGeometry(300+x, 360+y, 53, 38)
        self.greenStationsTop[15].setGeometry(200+x, 270+y, 53, 38)
        self.greenStationsTop[16].setGeometry(290+x, 230+y, 53, 38)
        self.greenStationsTop[17].setGeometry(300+x, 135+y, 53, 38)

    #initialize green station map features
    def make_red_stations(self,tab1):
        original_pixmap_station = QPixmap(add_TM+"images/Station.png")
        resized_pixmap_station = original_pixmap_station.scaled(53,38)
        original_pixmap_station_bot = QPixmap(add_TM+"images/StationBot.png")
        resized_pixmap_station_bot = original_pixmap_station_bot.scaled(53,38)
        self.redStationsTop = []
        self.redStationsBot = []
        for i in range(8):
            self.redStationsBot.append(QLabel(tab1))
            self.redStationsBot[i].setPixmap(resized_pixmap_station_bot)
            self.redStationsTop.append(QLabel(tab1))
            self.redStationsTop[i].setPixmap(resized_pixmap_station)
        self.redStationsBot[0].setGeometry(165, 40, 53, 38)
        self.redStationsBot[1].setGeometry(340, 85, 53, 38)
        self.redStationsBot[2].setGeometry(380, 155, 53, 38)
        self.redStationsBot[3].setGeometry(420, 85, 53, 38)
        self.redStationsBot[4].setGeometry(780, 220, 53, 38)
        self.redStationsBot[5].setGeometry(420, 310, 53, 38)
        self.redStationsBot[6].setGeometry(340, 310, 53, 38)
        self.redStationsBot[7].setGeometry(85, 315, 53, 38)

        self.redStationsTop[0].setGeometry(165, 40, 53, 38)
        self.redStationsTop[1].setGeometry(340, 85, 53, 38)
        self.redStationsTop[2].setGeometry(380, 155, 53, 38)
        self.redStationsTop[3].setGeometry(420, 85, 53, 38)
        self.redStationsTop[4].setGeometry(780, 220, 53, 38)
        self.redStationsTop[5].setGeometry(420, 310, 53, 38)
        self.redStationsTop[6].setGeometry(340, 310, 53, 38)
        self.redStationsTop[7].setGeometry(85, 315, 53, 38)

    #initialize traffic lights 
    def make_green_lights(self, tab1, x):
        original_pixmap_red = QPixmap(add_TM+"images/RedLight.png")
        resized_pixmap_red = original_pixmap_red.scaled(30,30)
        original_pixmap_green = QPixmap(add_TM+"images/GreenLight.png")
        resized_pixmap_green = original_pixmap_green.scaled(30,30)
        self.greenLightsBot = []
        self.greenLightsTop = []
        for i in range(10):
            self.greenLightsBot.append(QLabel(tab1))
            self.greenLightsTop.append(QLabel(tab1))
            self.greenLightsBot[i].setPixmap(resized_pixmap_red)
            self.greenLightsTop[i].setPixmap(resized_pixmap_green)   
            self.greenLightsBot[i].setGeometry(10+30*i, 10, 30, 30)
            self.greenLightsTop[i].setGeometry(10+30*i, 10, 30, 30)
        self.greenLightsBot[0].setGeometry(640, 200, 30, 30)
        self.greenLightsTop[0].setGeometry(640, 200, 30, 30)
        self.greenLightsBot[1].setGeometry(550, 150, 30, 30)
        self.greenLightsTop[1].setGeometry(550, 150, 30, 30)
        self.greenLightsBot[2].setGeometry(450, 150, 30, 30)
        self.greenLightsTop[2].setGeometry(450, 150, 30, 30)
        self.greenLightsBot[3].setGeometry(360, 197, 30, 30)
        self.greenLightsTop[3].setGeometry(360, 197, 30, 30)
        self.greenLightsBot[4].setGeometry(130, 35, 30, 30)
        self.greenLightsTop[4].setGeometry(130, 35, 30, 30)
        self.greenLightsBot[5].setGeometry(230, 400, 30, 30)
        self.greenLightsTop[5].setGeometry(230, 400, 30, 30)
        self.greenLightsBot[6].setGeometry(400, 400, 30, 30)
        self.greenLightsTop[6].setGeometry(400, 400, 30, 30)
        self.greenLightsBot[7].setGeometry(550, 345, 30, 30)
        self.greenLightsTop[7].setGeometry(550, 345, 30, 30)
        self.greenLightsBot[8].setGeometry(640, 455, 30, 30)
        self.greenLightsTop[8].setGeometry(640, 455, 30, 30)
        self.greenLightsBot[9].setGeometry(515, 345, 30, 30)
        self.greenLightsTop[9].setGeometry(515, 345, 30, 30)

    def make_green_temp(self, tab):
        self.greenTempButton = QPushButton("Set New Temperature", tab)
        self.greenTempButton.setStyleSheet("background-color: white; color: black;")
        self.greenTempButton.clicked.connect(self.send_green_temp_button_click)
        self.greenTempButton.setGeometry(470, 270, 125, 25)  

        self.greenNewTemp = QLineEdit(tab)
        self.greenNewTemp.setStyleSheet("background-color: white; color: black;")
        self.greenNewTemp.setGeometry(470, 240, 70, 25)

        self.greenTempLabel = QLabel('Temperature (F°): 70.0°', tab)
        self.greenTempLabel.setStyleSheet("color: white;")
        self.greenTempLabel.setGeometry(470, 220, 120, 20)
    
    def make_red_temp(self, tab):
        self.redTempButton = QPushButton("Set New Temperature", tab)
        self.redTempButton.setStyleSheet("background-color: white; color: black;")
        self.redTempButton.clicked.connect(self.send_red_temp_button_click)
        self.redTempButton.setGeometry(360, 260, 125, 25)  

        self.redNewTemp = QLineEdit(tab)
        self.redNewTemp.setStyleSheet("background-color: white; color: black;")
        self.redNewTemp.setGeometry(360, 230, 70, 25)

        self.redTempLabel = QLabel('Temperature (F°): 70.0°', tab)
        self.redTempLabel.setStyleSheet("color: white;")
        self.redTempLabel.setGeometry(360, 210, 120, 20)

    def send_green_temp_button_click(self):
        greenTemp = float(self.greenNewTemp.text())
        self.greenTempLabel.setText(f'Temperature(F°): {greenTemp}°')
        if greenTemp <= 32.0:
            [block.heater_on() for block in greenBlocks[:151]]
        else:
            [block.heater_off() for block in greenBlocks[:151]]
    
    def send_red_temp_button_click(self):
        redTemp = float(self.redNewTemp.text())
        self.redTempLabel.setText(f'Temperature(F°): {redTemp}°')
        if redTemp <= 32.0:
            [block.heater_on() for block in redBlocks[:77]]
        else:
            [block.heater_off() for block in redBlocks[:77]]

    #initialize temp train information label     
    # def make_train(self, tab3):
    #     self.trainLabel = QPushButton("Train Info", tab3)
    #     self.trainLabel.setStyleSheet("background-color: white; color: black;")
    #     self.trainLabel.setGeometry(50,40, 80, 25)

# Main entry to start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    upload_window = TrackUI()
    upload_window.show()
    sys.exit(app.exec())    