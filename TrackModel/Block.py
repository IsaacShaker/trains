from Beacon import Beacon
class Block:
    def __init__(self, line, section, number, length, grade, speedLimit, elevation, cumElevation):
        self.line = line
        self.section = section
        self.number = number
        self.nextBlock = None
        self.length = length
        self.grade = grade
        self.speedLimit = speedLimit
        self.elevation = elevation
        self.cumElevation = cumElevation
        self.occupied = False
        self.beacon = None

    def display_info(self, index):
        if self.nextBlock == 0:
            return f"Block {index}:\n\tLine: {self.line} \n\tSection: {self.section} \n\tBlock Number: {self.number} \n\tBlock Length: {self.length} \n\tBlock Grade: {self.grade} \n\tSpeed Limit: {self.speedLimit} \n\tElevation: {self.elevation} \n\tCumulative Elevation: {self.cumElevation} \n\tOccupied: {self.occupied}"
        else:
            return f"Block {index}:\n\tLine: {self.line} \n\tSection: {self.section} \n\tBlock Number: {self.number} \n\tNext Block: {self.nextBlock.display_num()} \n\tBlock Length: {self.length} \n\tBlock Grade: {self.grade} \n\tSpeed Limit: {self.speedLimit} \n\tElevation: {self.elevation} \n\tCumulative Elevation: {self.cumElevation} \n\tOccupied: {self.occupied}"

    def display_num(self):
        return f"{self.number}"

    def get_num(self):
        return self.number

    def get_occupied(self):
        return self.occupied
    
    def change_occupied(self):
        if(self.occupied):
            self.occupied = False
        else:
            self.occupied = True

    def set_O(self):
        self.occupied = True

    def set_N(self):
        self.occupied = False
    
    def set_next_block(self, nBlock):
        if isinstance(nBlock, Block):
            self.nextBlock = nBlock
        else:
            print("Not a block")

    def get_next_block(self):
        return self.nextBlock, self.length
    
    def if_occupied(self, train):
        if (self.occupied):
            auth = train.get_auth()
            if isinstance(self.beacon, Beacon):
                train.set_staticData(self.beacon.get_staticData())
            if self.number == 0:
                authority = 470
                speed = 40
                train.set_info(authority, speed)
            else:
                if auth <= 0:
                    authority = 0
                    speed = 0
                    train.set_info(authority, speed)
                else:
                    speed = 30
                    train.set_speed(speed)
    
    def set_beacon(self, beacon):
        self.beacon = beacon