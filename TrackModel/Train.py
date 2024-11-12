launcher = False
import requests
if launcher:
    from TrackModel.Station import Station
else:
    from Station import Station
class Train:
    def __init__(self, fLocOnBlock, fBlock, length):
        self.id = 0
        self.fLocOnBlock = fLocOnBlock
        self.fBlock = fBlock
        self.fBlockPrevious = fBlock
        self.bLocOnBlock = fLocOnBlock+length
        self.bBlock = fBlock
        self.station = None
        self.length = length
        self.fBackwards = False
        self.bBackwards = False
        self.speed = 200
        self.authority = 10000
        self.staticData = "No Data"
        self.dict_arr = None

        self.trainAuth = None
        self.trainCmd = None
        
    def display_info(self,index):
        string = f"Train {index}: \n\tFront Location: {self.fLocOnBlock} \n\tFront Block: {self.fBlock.display_num()} \n\tPrevious Front Block: {self.fBlockPrevious.display_num()} \n\tBack Location: {self.bLocOnBlock} \n\tBack Block: {self.bBlock.display_num()}\n\tLength: {self.length} \n\tSpeed: {self.speed} \n\tAuthority: {self.authority} \n\tStatic Data: {self.staticData}"
        return string
    
    def moveTrain(self, speed): #dict_arr
        #self.dict_arr = dict_arr
        if self.fBlock.get_num() == 85 and self.fBlockPrevious.get_num() == 100:
            self.fBackwards = True 
        elif self.fBlock.get_num() == 101 and self.fBlockPrevious.get_num() == 77:
            self.fBackwards = False
        elif self.fBlock.get_num() == 28 and self.fBlockPrevious.get_num() == 150:
            self.fBackwards = True
        elif self.fBlock.get_num() == 1 and self.fBlockPrevious.get_num() == 13:
            self.fBackwards = False

        # data_dict = None
        # response = requests.get('http://127.0.0.1:5000/train-model/get-data/current-speed')
        # if response.status_code == 200:
        #     data_dict = response.json()  # This converts the JSON response to a Python dictionary
        #     print("Received dictionary:", data_dict)
        # else:
        #     print("Failed to retrieve data:", response.text)

        if self.authority <= 0:
            self.authority = 0
            self.speed = 0
            self.fBlock.set_train(self, False)
            self.bBlock.set_train(self, True)
        else:
            mpsSpeed = (self.speed*1000)/60/60/1000
            self.authority = self.authority - mpsSpeed
            self.moveFront(mpsSpeed)
            self.syncBack()
        self.trainAuth = self.fBlock.authority
        self.trainCmd = self.fBlock.commandedSpeed

    def moveFront(self, mpsSpeed):
        if self.fLocOnBlock > 0:
            self.fLocOnBlock = self.fLocOnBlock - mpsSpeed
            self.fBlock.set_train(self, False)
        else:
            
            self.fBlock.train_set_beacon(self)
            remainingDistance = self.fLocOnBlock
            if self.fBackwards:
                self.fBlock.set_train(None, False)
                self.fBlockPrevious = self.fBlock
                self.fBlock, self.fLocOnBlock = self.fBlock.get_previous_block()
                self.fLocOnBlock += remainingDistance
                self.fBlock.set_train(self, False)
            else:
                self.fBlock.set_train(None, False)
                self.fBlockPrevious = self.fBlock
                self.fBlock, self.fLocOnBlock = self.fBlock.get_next_block()
                self.fLocOnBlock += remainingDistance
                self.fBlock.set_train(self, False)

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
    
