import requests
URL = 'http://127.0.0.1:5000'
launcher = True
if launcher:
    from TrackModel.Beacon import Beacon
    from TrackModel.RailroadCrossing import RailroadCrossing
    from TrackModel.Station import Station
    from TrackModel.Switch import Switch
    from TrackModel.Train import Train
else:
    from Beacon import Beacon
    from RailroadCrossing import RailroadCrossing
    from Station import Station
    from Switch import Switch
    from Train import Train

class Block:
    def __init__(self, line, section, number, length, grade, speedLimit, elevation, cumElevation, underground, commandedSpeed):
        self.line = line
        self.section = section
        self.number = number
        self.nextBlock = None
        self.previousBlock = None
        self.length = length
        self.grade = grade
        self.speedLimit = speedLimit
        self.elevation = elevation
        self.cumElevation = cumElevation
        self.underground = underground

        self.closed = False
        self.brokenTrack = False
        self.circuitFailure = False
        self.powerFailure = False
        self.trackHeater = False

        self.occupancy = False

        self.beacon = None
        self.station = None
        self.railroad = None
        self.switch = None
        self.train = None

        self.authority = None
        self.commandedSpeed = commandedSpeed

        self.beacon_data = {
            'id' : None,
            'beacon_info' : None
        }

    def get_table_data(self, index):
        if index == 0:
            return str(self.number)
        elif index == 1:
            return str(isinstance(self.train, Train))
        elif index == 2:
            return str(self.authority)
        elif index == 3:
            return str(self.commandedSpeed)
        elif index == 4:
            if isinstance(self.beacon, Beacon):
                return str(self.beacon.get_staticData())
            else:
                return ""
        elif index == 5:
            if isinstance(self.station, Station):
                return str(self.station.get_name())
            else:
                return ""
        elif index == 6:
            if isinstance(self.railroad, RailroadCrossing):
                return str(self.railroad.get_status())
            else:
                return ""
        elif index == 7:
            if isinstance(self.switch, Switch):
                return str(self.switch.get_LandR())
            else:
                return ""
        elif index == 8:
            if isinstance(self.nextBlock, Block):
                return str(self.nextBlock.get_num())
            else:
                return "None"
        elif index == 9:
            if isinstance(self.previousBlock, Block):
                return str(self.previousBlock.get_num())
            else:
                return "None"
        elif index == 10:
            return str(self.length)
        elif index == 11:
            return str(self.grade)
        elif index == 12:
            return str(self.speedLimit)
        elif index == 13:
            return str(self.elevation)
        elif index == 14:
            return str(self.cumElevation)
        elif index == 15:
            return str(self.underground)
        elif index == 16:
            return str(self.brokenTrack)
        elif index == 17:
            return str(self.circuitFailure)
        elif index == 18:
            return str(self.powerFailure)
        else:
            return ""    
    def display_info(self, index):
        if self.nextBlock == 0:
            return f"Block {index}:\n\tLine: {self.line}\n\tBlock Number: {self.number} \n\tBlock Length: {self.length} \n\tBlock Grade: {self.grade} \n\tSpeed Limit: {self.speedLimit} \n\tElevation: {self.elevation} \n\tCumulative Elevation: {self.cumElevation} \n\tOccupied: {self.occupied}\n\tBroken Track: {self.brokenTrack}\n\tTrack Circuit Failure: {self.circuitFailure}\n\tPower Failure: {self.powerFailure}"
        else:
            return f"Block {index}:\n\tLine: {self.line}\n\tBlock Number: {self.number} \n\tNext Block: {self.nextBlock.display_num()} \n\tBlock Length: {self.length} \n\tBlock Grade: {self.grade} \n\tSpeed Limit: {self.speedLimit} \n\tElevation: {self.elevation} \n\tCumulative Elevation: {self.cumElevation} \n\tOccupied: {self.occupied}\n\tBroken Track: {self.brokenTrack}\n\tTrack Circuit Failure: {self.circuitFailure}\n\tPower Failure: {self.powerFailure}"
    def display_num(self):
        return f"{self.number}"  
    def get_if_train(self):
        if isinstance(self.train, Train):
            return True
        return False

    def set_train(self, train, FOrB, diff):
        if isinstance(train, Train):
            self.train = train
            if self.authority != None and not FOrB:
                self.train.set_auth(self.authority)
            if self.commandedSpeed != None and not FOrB:
                self.train.set_speed(self.commandedSpeed)
            if isinstance(self.station, Station) and (self.train.get_fLocOnBlock() > (self.length/2) - 17.1) and (self.train.get_fLocOnBlock() < (self.length/2) - 15.1) and diff == 0:
                self.station.set_trainIn(True)
            else:
                if isinstance(self.station, Station):
                    self.station.set_trainIn(False)
        else:
            self.train = None

    def train_set_beacon(self, train):
        if isinstance(self.beacon, Beacon):
            self.beacon_data["id"]=train.get_id()
            self.beacon_data["beacon_info"]=str(self.beacon.get_staticData())
            train.set_staticData(self.beacon.get_staticData())

           # print("beacon info:" + self.beacon.get_staticData())
            response = requests.post(URL + '/train-model/get-data/beacon-info', json=self.beacon_data)

            
    def set_occupancies(self):
        if isinstance(self.train, Train) or self.brokenTrack or self.circuitFailure or self.powerFailure or self.closed:
            self.occupancy = True
        else:
            self.occupancy = False
    def set_O(self):
        self.occupied = True
    def set_N(self):
        self.occupied = False
    def set_next_block(self, nBlock):
        if isinstance(nBlock, Block):
            self.nextBlock = nBlock
    def set_previous_block(self, pBlock):
        if isinstance(pBlock, Block):
            self.previousBlock = pBlock
    def set_authority(self, auth):
        self.authority = auth
    def set_cmd_speed(self, cmd):
        self.commandedSpeed = cmd
    def set_beacon(self, beacon):
        self.beacon = beacon
    def set_station(self, station):
        self.station = station
    def set_railroad(self, railroad):
        self.railroad = railroad
    def set_switch(self, switch):
        self.switch = switch
    def set_traffic(self, traffic):
        self.trafficLight = traffic

    def get_num(self):
        return self.number
    def get_length(self):
        return self.length
    def get_occupied(self):
        return self.occupied
    def get_broken(self):
        return self.brokenTrack
    def get_circuit(self):
        return self.circuitFailure
    def get_power(self):
        return self.powerFailure
    def get_heater(self):
        return self.trackHeater
    def get_previous_block(self):
        return self.previousBlock, self.previousBlock.get_length()
    def get_next_block(self):
        return self.nextBlock, self.nextBlock.get_length()
    def get_station(self):
        return self.station
    def get_closed(self):
        return self.closed
    def get_grade(self):
        return self.grade

    def change_broken(self):
        if (self.brokenTrack):
            self.brokenTrack = False
        else:
            self.brokenTrack = True
    def change_circuit(self):
        if (self.circuitFailure):
            self.circuitFailure = False
        else:
            self.circuitFailure = True
    def change_power(self):
        if (self.powerFailure):
            self.powerFailure = False
        else:
            self.powerFailure = True
    
    def heater_on(self):
        self.trackHeater = True
    def heater_off(self):
        self.trackHeater = False