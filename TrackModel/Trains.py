

class Trains:
    def __init__(self):
        self.trainList = []
        self.speeds = []
        self.authorities = []
        self.commandedSpeeds = []

    def addTrain(self, train):
        self.trainList.append(train)
        self.speeds.append(0.0)
        self.authorities.append(0.0)
        self.commandedSpeeds.append(0.0)
    
    def moveTrains(self):
        for i in range(len(self.trainList)):
            self.trainList[i].moveTrain(self.speeds[i])
            self.authorities[i] = self.trainList[i].get_auth()
            self.commandedSpeeds[i] = self.trainList[i].get_speed()
        
    def set_indexed_speed(self, index, speed):
        self.speeds[index] = speed