class Train:
    def __init__(self, fLocOnBlock, fBlock, length, speed):
        self.fLocOnBlock = fLocOnBlock
        self.fBlock = fBlock
        self.bLocOnBlock = fLocOnBlock+length
        self.bBlock = fBlock
        self.length = length
        self.speed = 50
        self.authority = 1000
        self.staticData = "No Data"
        
    def display_info(self,index):
        string = f"Train {index}: \n\tFront Location: {self.fLocOnBlock} \n\tFront Block: {self.fBlock.display_num()} \n\tBack Location: {self.bLocOnBlock} \n\tBack Block: {self.bBlock.display_num()} \n\tLength: {self.length} \n\tSpeed: {self.speed} \n\tAuthority: {self.authority} \n\tStatic Data: {self.staticData}"
        return string
    
    def moveTrain(self):
        mpsspeed = (self.speed*1000)/60/60/10
        self.authority = self.authority - mpsspeed
        if self.authority == 0:
            self.speed = 0
        if self.fLocOnBlock > 0:
            self.fLocOnBlock = self.fLocOnBlock - mpsspeed
            self.fBlock.set_O()
        else:
            self.fBlock.set_N()
            self.fBlock, self.fLocOnBlock = self.fBlock.get_next_block()
            self.fBlock.set_O()
        if self.bLocOnBlock > 0:
            self.bLocOnBlock = self.bLocOnBlock - mpsspeed
            self.bBlock.set_O()
        else:
            self.bBlock.set_N()
            self.bBlock, self.bLocOnBlock = self.bBlock.get_next_block()
            self.bBlock.set_O()

    def set_info(self, authority, speed):
        self.authority = authority
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed

    def get_auth(self):
        return self.authority
    
    def set_staticData(self, stData):
        self.staticData = stData
    
