import pandas as pd
from Block import Block
from Switch import Switch
from RailroadCrossing import RailroadCrossing
from TrafficLight import TrafficLight
from Beacon import Beacon
from Train import Train
from Station import Station

def buildTrack():
    #Yard 
    Yard = Block('Blue', 'Yard', 0, 50, 0, 100, 0, 0)
    Yard.set_next_block(Yard)
    #Create Blocks
    blueBlocks = []
    #Read block data from excel file
    df = pd.read_excel('BlueLine.xlsx', sheet_name='Sheet1')
    for index, row in df.iterrows():
        line = row['Line']
        section = row['Section']
        number = row['Block Number']
        length = row['Block Length (m)']
        grade = row['Block Grade (%)']
        speedLimit = row['Speed Limit (Km/Hr)']
        elevation = row['ELEVATION (M)']
        cumElevation = row['CUMALTIVE ELEVATION (M)']
        blueBlocks.append(Block(line, section, number, length, grade, speedLimit, elevation, cumElevation))
    Yard.set_next_block(blueBlocks[0])
    blueBlocks[0].set_next_block(blueBlocks[1])
    blueBlocks[1].set_next_block(blueBlocks[2])
    blueBlocks[2].set_next_block(blueBlocks[3])
    blueBlocks[3].set_next_block(blueBlocks[4])
    blueBlocks[4].set_next_block(blueBlocks[5])
    blueBlocks[5].set_next_block(blueBlocks[6])
    blueBlocks[6].set_next_block(blueBlocks[7])
    blueBlocks[7].set_next_block(blueBlocks[8])
    blueBlocks[8].set_next_block(blueBlocks[9])
    blueBlocks[9].set_next_block(Yard)
    blueBlocks[10].set_next_block(blueBlocks[11])
    blueBlocks[11].set_next_block(blueBlocks[12])
    blueBlocks[12].set_next_block(blueBlocks[13])
    blueBlocks[13].set_next_block(blueBlocks[14])
    blueBlocks[14].set_next_block(Yard)



    #Create Switch
    #Block 5, Block 6, Block 11
    blueSwitch = Switch("Blue", "A", blueBlocks[4], blueBlocks[5], blueBlocks[10], False)

    #Create Railroad 
    #Block 3
    blueRailroadCrossing = RailroadCrossing("Blue", "A", blueBlocks[2], False)

    #Create Traffic Lights
    blueTrafficLights = []
    #Block 6
    blueTrafficLights.append(TrafficLight("Blue", "B", blueBlocks[5], False))
    #Block 11
    blueTrafficLights.append(TrafficLight("Blue", "B", blueBlocks[10], False))

    #Create Beacons
    blueBeacons = []
    #Block 9
    blueBeacons.append(Beacon("Blue", "B", blueBlocks[8], "Station B"))
    blueBlocks[8].set_beacon(blueBeacons[0])
    #Block 14
    blueBeacons.append(Beacon("Blue", "C", blueBlocks[13], "Station C"))
    blueBlocks[13].set_beacon(blueBeacons[1])

    #Train
    blueTrain = Train(10, Yard, 20, 100)
    
    #Stations
    blueStations = []
    blueStations.append(Station('Station B', 'Blue' , 'B', blueBlocks[9], 1, 0))
    blueStations.append(Station('Station C', 'Blue' , 'B', blueBlocks[14], 1, 0))

    return Yard, blueBlocks, blueSwitch, blueRailroadCrossing, blueTrafficLights, blueBeacons, blueTrain, blueStations