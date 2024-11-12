class Trains:
    def __init__(self):
        self.trainList = []
        self.speeds = []

    def addTrain(self, train):
        self.trainList.append(train)
        self.speeds.append(0.0)
    
    def moveTrains(self):
        #get speeds from aidan
        for i in range(len(self.trainList)):
            self.trainList[i].moveTrain(self.speeds[i])