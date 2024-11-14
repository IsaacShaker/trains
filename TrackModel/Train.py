launcher = True
import requests
URL = 'http://127.0.0.1:5000'
if launcher:
    from TrackModel.Station import Station
else:
    from Station import Station
class Train:
    def __init__(self, fLocOnBlock, fBlock, length, id):
        self.id = id
        self.fLocOnBlock = fLocOnBlock
        self.fBlock = fBlock
        self.fBlockPrevious = fBlock
        self.bLocOnBlock = fLocOnBlock+length
        self.bBlock = fBlock
        self.station = None
        self.length = length
        self.fBackwards = False
        self.bBackwards = False
        self.staticData = "No Data"
        self.speed = 0
        self.authority = None
        self.commandedSpeed = None
        self.grade_info = {
            'id' : None,
            'grade' : None
        }
        
    def display_info(self,index):
        string = f"Train {index}: \n\tFront Location: {self.fLocOnBlock} \n\tFront Block: {self.fBlock.display_num()} \n\tPrevious Front Block: {self.fBlockPrevious.display_num()} \n\tBack Location: {self.bLocOnBlock} \n\tBack Block: {self.bBlock.display_num()}\n\tLength: {self.length} \n\tSpeed: {self.speed} \n\tAuthority: {self.authority} \n\tStatic Data: {self.staticData}"
        return string
    
    def moveTrain(self, diff):
        if self.fBlock.get_num() == 85 and self.fBlockPrevious.get_num() == 100:
            self.fBackwards = True 
        elif self.fBlock.get_num() == 101 and self.fBlockPrevious.get_num() == 77:
            self.fBackwards = False
        elif self.fBlock.get_num() == 28 and self.fBlockPrevious.get_num() == 150:
            self.fBackwards = True
        elif self.fBlock.get_num() == 1 and self.fBlockPrevious.get_num() == 13:
            self.fBackwards = False

        if diff == None:
            diff = 0
        self.moveFront(diff)
        self.syncBack()

    def moveFront(self, authDiff):
        if self.fLocOnBlock > 0:
            self.fLocOnBlock -= authDiff
            self.fBlock.set_train(self, False)
        else:
            self.fBlock.train_set_beacon(self)
            remainingDistance = self.fLocOnBlock
            if self.fBackwards:
                self.fBlock.set_train(None, False)
                self.fBlockPrevious = self.fBlock
                self.fBlock, self.fLocOnBlock = self.fBlock.get_previous_block()
                self.fLocOnBlock += remainingDistance
                self.fLocOnBlock -= authDiff
                self.fBlock.set_train(self, False)
            else:
                self.fBlock.set_train(None, False)
                self.fBlockPrevious = self.fBlock
                self.fBlock, self.fLocOnBlock = self.fBlock.get_next_block()
                self.fLocOnBlock += remainingDistance
                self.fLocOnBlock -= authDiff
                self.fBlock.set_train(self, False)
        self.grade_info["id"]=self.id
        self.grade_info["grade_info"]=self.fBlock.get_grade()
        response = requests.post(URL + "/train-model/get-data/grade-info", json=self.grade_info)
        print(f"LocOnBLock: {self.fLocOnBlock}")
            

    def syncBack(self):
        self.bLocOnBlock = self.fLocOnBlock + self.length
        if self.bLocOnBlock > self.fBlock.get_length():
            self.bBlock.set_train(None, True)
            if self.bBackwards:
                if self.bLocOnBlock <= 0:
                    self.bBlock, self.bLocOnBlock = self.bBlock.get_previous_block()
            else:
                if self.bLocOnBlock <= 0:
                    self.bBlock, self.bLocOnBlock = self.bBlock.get_next_block()

            self.bLocOnBlock = self.length - (self.fBlock.get_length() - self.fLocOnBlock)
            self.bBlock.set_train(self, True)
        else:
            self.bBlock.set_train(None, True)
            self.bBlock = self.fBlock
            self.bBlock.set_train(self, True)
            
    def set_info(self, authority, speed):
        self.authority = authority
        self.speed = speed
    def set_auth(self, auth):
        self.authority = auth
    def set_speed(self, speed):
        self.speed = speed
    def set_staticData(self, stData):
        self.staticData = stData

    def get_fLocOnBlock(self):
        return self.fLocOnBlock
    def get_auth(self):
        return self.authority
    def get_speed(self):
        return self.speed
    def get_id(self):
        return self.id
    
