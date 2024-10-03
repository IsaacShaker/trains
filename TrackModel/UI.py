import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QWidget, QLineEdit, QComboBox, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
from TrackModel import buildTrack

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Make a PyQt Window
        self.setWindowTitle("Track Model UI")
        self.setGeometry(100,100,800,350)
        self.setStyleSheet("background-color: grey")

        #Makes tabs for the windows
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.create_tabs()

        self.train_timer = QTimer()
        self.train_timer.timeout.connect(blueTrain.moveTrain)
        for i in range(16):
            if i == 0:
                self.train_timer.timeout.connect(lambda: Yard.if_occupied(blueTrain))
            else:
                self.train_timer.timeout.connect(lambda i=i: blueBlocks[i-1].if_occupied(blueTrain))
        self.train_timer.start(100)

    def create_tabs(self):
        #Create Tab1
        tab1 = QWidget()
        self.tab_widget.addTab(tab1, "Main Tab")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        #self.temp_buttons(tab1)

        self.make_blocks(tab1, 110)

        self.make_switch(tab1, 110)

        self.make_lights(tab1, 110)

        self.make_crossing(tab1, 110)

        self.make_train(tab1)

        self.make_stations(tab1)

        self.make_beacons(tab1)

        # Tab 2 Example Tab for Now
        tab2 = QWidget()
        self.tab_widget.addTab(tab2, "Test Bench")
        self.tab_widget.setStyleSheet("background-color: #444444; color: white;")

        self.make_test_bench_buttons(tab2, -30)
    
    def on_button_click(self):
        print("Button clicked!")

    def button1_click(self):
        blueBlocks[0].change_occupied()

    def button3_click(self):
        blueSwitch.change_LorR()

    def button4_click(self):
        blueTrafficLights[0].change_RorG()

    def button5_click(self):
        blueRailroadCrossing.change_UorD()

    def update_ui(self):
        #Constantly update block color based on occupied variable
        for i in range(15):
            if blueBlocks[i].get_occupied():
                self.blockArrows[i].hide()
            else:
                self.blockArrows[i].show()
            index = i+1
            self.blockArrows[i].setToolTip(blueBlocks[i].display_info(index))
            self.whiteArrows[i].setToolTip(blueBlocks[i].display_info(index))
        #Constantly update switch direction based on left or right variable
        if blueSwitch.get_LorR():
            self.switchLeft.hide()
            self.switchRight.show()
        else:
            self.switchLeft.show()
            self.switchRight.hide()
        self.switchLeft.setToolTip(blueSwitch.display_info(0))
        self.switchRight.setToolTip(blueSwitch.display_info(0))
        #Constantly update traffic light color based on red or green variable
        for i in range(2):
            if blueTrafficLights[i].get_RorG():
                self.greenLight[i].show()
            else:
                self.greenLight[i].hide()
            self.greenLight[i].setToolTip(blueTrafficLights[i].display_info(i))
            self.redLight[i].setToolTip(blueTrafficLights[i].display_info(i))
            
        #Constantly update railroad crossing color based on up or down variable
        if blueRailroadCrossing.get_UorD():
            self.greenCrossing.hide()
        else:
            self.greenCrossing.show()
        self.greenCrossing.setToolTip(blueRailroadCrossing.display_info(0))
        self.redCrossing.setToolTip(blueRailroadCrossing.display_info(0))

        self.trainLabel.setToolTip(blueTrain.display_info(0))

        self.stations[0].setToolTip(blueStations[0].display_info())
        self.stations[1].setToolTip(blueStations[1].display_info())

        self.beacons[0].setToolTip(blueBeacons[0].display_info())
        self.beacons[1].setToolTip(blueBeacons[1].display_info())

    def temp_buttons(self, tab1):
        button1 = QPushButton("Change Block 1 Occupancy", tab1)
        button1.setStyleSheet("background-color: white; color: black;")
        button1.clicked.connect(self.button1_click)
        button1.setGeometry(50, 50, 150, 20)

        button3 = QPushButton("Change Switch State", tab1)
        button3.setStyleSheet("background-color: white; color: black;")
        button3.clicked.connect(self.button3_click)
        button3.setGeometry(50, 75, 150, 20)

        button4 = QPushButton("Change Traffic Light 1", tab1)
        button4.setStyleSheet("background-color: white; color: black;")
        button4.clicked.connect(self.button4_click)
        button4.setGeometry(50, 100, 150, 20)

        button5 = QPushButton("Change Railroad Crossing", tab1)
        button5.setStyleSheet("background-color: white; color: black;")
        button5.clicked.connect(self.button5_click)
        button5.setGeometry(50, 125, 150, 20)

    def make_test_bench_buttons(self, tab2, x):
        idStrings = ['Switch ID', 'Crossing Light ID', 'Traffic Light ID', 'Block ID', 'Block ID', 'Block ID']
        self.idLabels = []
        self.idInputs = []
        varStrings = ['Left or Right', 'Crossing Light ID', 'Traffic Light ID', 'Block ID', 'Block ID', 'Block ID']
        self.varLabels = []
        self.varInputs = []
        self.sendButtons = [] 
        for i in range(6):
            self.idLabels.append(QLabel(idStrings[i], tab2))
            self.idLabels[i].setStyleSheet("color: white;")
            self.idLabels[i].setGeometry(10-x, 40 + 40 * i, 100, 20)

            self.idInputs.append(QLineEdit(tab2))
            self.idInputs[i].setStyleSheet("background-color: white; color: black;")
            self.idInputs[i].setGeometry(10-x, 60 + 40 * i, 90, 20)

            self.varLabels.append(QLabel(varStrings[i], tab2))
            self.varLabels[i].setStyleSheet("color: white;")
            self.varLabels[i].setGeometry(110-x, 40 + 40 * i, 90, 20)

            self.sendButtons.append(QPushButton("Send", tab2))
            self.sendButtons[i].setStyleSheet("background-color: white; color: black;")
            self.sendButtons[i].clicked.connect(lambda _, index=i: self.sendButton_click(index))
            self.sendButtons[i].setGeometry(220-x, 60 + 40 * i, 50, 20)           

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

    def sendButton_click(self, i):
        id = int(self.idInputs[i].text())
        if (i == 3 or i == 4):
            var = self.varInputs[i].text()
        else:
            var = self.varInputs[i].currentText()
        if i == 0:
            if id == 0:
                if var == "Left":
                    blueSwitch.set_L()
                else:
                    blueSwitch.set_R()
            else:
                print("Index Error sendButton_click function.")
        elif i == 1:
            if id == 0:
                if var == "Up":
                    blueRailroadCrossing.set_U()
                else:
                    blueRailroadCrossing.set_D()
            else:
                print("Index Error sendButton_click function.")
        elif i == 2:
            if id <= 1 and id >= 0:
                if var == "Red":
                    blueTrafficLights[id].set_R()
                else:
                    blueTrafficLights[id].set_G()
            else:
                print("Index Error sendButton_click function.")

        elif i == 3:
            if id <= 15 and id >= 1:
                print(f"Authority on block {id} set to {var} m")
            else:
                print("error")
        elif i == 4:
            if id <= 15 and id >= 1:
                print(f"Commanded Speed on block {id} set to {var} km/h")
            else:
                print("Index Error sendButton_click function.")
        elif i == 5:
            if id <= 15 and id >= 1:
                if var == "Occupied":
                    blueBlocks[id-1].set_O()
                else:
                    blueBlocks[id-1].set_N()
            else:
                print("Index Error sendButton_click function.")

    def make_blocks(self, tab1, x):
        #White arrows are behind blue arrows so you can show or hide the blue arrows
        self.whiteArrows = []
        original_pixmap_white = QPixmap("images/WhiteFlatArrow.png")
        resized_pixmap_white = original_pixmap_white.scaled(60,30)
        for i in range(15):
            self.whiteArrows.append(QLabel(tab1))
            self.whiteArrows[i].setPixmap(resized_pixmap_white)
        self.whiteArrows[0].setGeometry(50, 250-x, 60, 30)
        self.whiteArrows[1].setGeometry(110, 250-x, 60, 30)
        self.whiteArrows[2].setGeometry(170, 250-x, 60, 30)
        self.whiteArrows[3].setGeometry(230, 250-x, 60, 30)
        self.whiteArrows[4].setGeometry(290, 250-x, 60, 30)
        self.whiteArrows[5].setGeometry(430, 200-x, 60, 30)
        self.whiteArrows[6].setGeometry(490, 200-x, 60, 30)
        self.whiteArrows[7].setGeometry(550, 200-x, 60, 30)
        self.whiteArrows[8].setGeometry(610, 200-x, 60, 30)
        self.whiteArrows[9].setGeometry(670, 200-x, 60, 30)
        self.whiteArrows[10].setGeometry(430, 300-x, 60, 30)
        self.whiteArrows[11].setGeometry(490, 300-x, 60, 30)
        self.whiteArrows[12].setGeometry(550, 300-x, 60, 30)
        self.whiteArrows[13].setGeometry(610, 300-x, 60, 30)
        self.whiteArrows[14].setGeometry(670, 300-x, 60, 30)

        self.blockArrows = []
        original_pixmap_blue = QPixmap("images/BlueFlatArrow.png")
        resized_pixmap_blue = original_pixmap_blue.scaled(60,30)
        for i in range(15):
            self.blockArrows.append(QLabel(tab1))
            self.blockArrows[i].setPixmap(resized_pixmap_blue)
        self.blockArrows[0].setGeometry(50, 250-x, 60, 30)
        self.blockArrows[1].setGeometry(110, 250-x, 60, 30)
        self.blockArrows[2].setGeometry(170, 250-x, 60, 30)
        self.blockArrows[3].setGeometry(230, 250-x, 60, 30)
        self.blockArrows[4].setGeometry(290, 250-x, 60, 30)
        self.blockArrows[5].setGeometry(430, 200-x, 60, 30)
        self.blockArrows[6].setGeometry(490, 200-x, 60, 30)
        self.blockArrows[7].setGeometry(550, 200-x, 60, 30)
        self.blockArrows[8].setGeometry(610, 200-x, 60, 30)
        self.blockArrows[9].setGeometry(670, 200-x, 60, 30)
        self.blockArrows[10].setGeometry(430, 300-x, 60, 30)
        self.blockArrows[11].setGeometry(490, 300-x, 60, 30)
        self.blockArrows[12].setGeometry(550, 300-x, 60, 30)
        self.blockArrows[13].setGeometry(610, 300-x, 60, 30)
        self.blockArrows[14].setGeometry(670, 300-x, 60, 30)

        #this is the timer that constantly updates the states for all of the components 
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)

    def make_switch(self, tab1, x):
        original_pixmap_left = QPixmap("images/SwitchLeft.png")
        resized_pixmap_left = original_pixmap_left.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.switchLeft = QLabel(tab1)
        self.switchLeft.setPixmap(resized_pixmap_left)
        self.switchLeft.setGeometry(350, 203-x, 80, 125)

        original_pixmap_right = QPixmap("images/SwitchRight.png")
        resized_pixmap_right = original_pixmap_right.scaled(90,125, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.switchRight = QLabel(tab1)
        self.switchRight.setPixmap(resized_pixmap_right)
        self.switchRight.setGeometry(350, 203-x, 80, 125)

    def make_lights(self, tab1, x):
        original_pixmap_red = QPixmap("images/RedLight.png")
        resized_pixmap_red = original_pixmap_red.scaled(40,40)
        original_pixmap_green = QPixmap("images/GreenLight.png")
        resized_pixmap_green = original_pixmap_green.scaled(40,40)
        self.redLight = []
        self.greenLight = []
        self.redLight.append(QLabel(tab1))
        self.redLight.append(QLabel(tab1))
        self.redLight[0].setPixmap(resized_pixmap_red)
        self.redLight[1].setPixmap(resized_pixmap_red)
        self.redLight[0].setGeometry(435, 150-x, 40, 40)
        self.redLight[1].setGeometry(435, 340-x, 40, 40)
        self.greenLight.append(QLabel(tab1))
        self.greenLight.append(QLabel(tab1))
        self.greenLight[0].setPixmap(resized_pixmap_green)
        self.greenLight[1].setPixmap(resized_pixmap_green)
        self.greenLight[0].setGeometry(435, 150-x, 40, 40)
        self.greenLight[1].setGeometry(435, 340-x, 40, 40)

    def make_crossing(self, tab1, x):
        original_pixmap_red = QPixmap("images/RedCrossing.png")
        resized_pixmap_red = original_pixmap_red.scaled(50,50)
        original_pixmap_green = QPixmap("images/GreenCrossing.png")
        resized_pixmap_green = original_pixmap_green.scaled(50,50)

        self.redCrossing = QLabel(tab1)
        self.redCrossing.setPixmap(resized_pixmap_red)
        self.redCrossing.setGeometry(175, 195-x, 50, 50)
        self.greenCrossing = QLabel(tab1)
        self.greenCrossing.setPixmap(resized_pixmap_green)
        self.greenCrossing.setGeometry(175, 195-x, 50, 50)
    
    def make_train(self, tab1):
        self.trainLabel = QPushButton("Train Info", tab1)
        self.trainLabel.setStyleSheet("background-color: white; color: black;")
        self.trainLabel.setGeometry(50, 200, 80, 20)

    def make_stations(self,tab1):
        original_pixmap_station = QPixmap("images/Station.png")
        resized_pixmap_station = original_pixmap_station.scaled(53,38)
        self.stations = []
        self.stations.append(QLabel(tab1))
        self.stations[0].setPixmap(resized_pixmap_station)
        self.stations[0].setGeometry(670, 40, 53, 38)

        self.stations.append(QLabel(tab1))
        self.stations[1].setPixmap(resized_pixmap_station)
        self.stations[1].setGeometry(670, 225, 53, 38)

    def make_beacons(self, tab1):
        original_pixmap_beacon = QPixmap("images/Beacon.png")
        resized_pixmap_beacon = original_pixmap_beacon.scaled(40,60)
        self.beacons = []
        self.beacons.append(QLabel(tab1))
        self.beacons[0].setPixmap(resized_pixmap_beacon)
        self.beacons[0].setGeometry(617, 30, 40, 60)

        self.beacons.append(QLabel(tab1))
        self.beacons[1].setPixmap(resized_pixmap_beacon)
        self.beacons[1].setGeometry(617, 221, 40, 60)

if __name__ == "__main__":

    Yard, blueBlocks, blueSwitch, blueRailroadCrossing, blueTrafficLights, blueBeacons, blueTrain, blueStations =buildTrack()
    app = QApplication(sys.argv)  
    window = MainWindow()          
    window.show()                  
    sys.exit(app.exec())           