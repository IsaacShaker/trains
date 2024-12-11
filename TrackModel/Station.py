import random
class Station:
    def __init__(self, name, line, section, number, Left, Right):
        self.name = name
        self.line = line
        self.section = section
        self.block = number
        self.trainIn = False
        self.leftDoor = Left
        self.rightDoor = Right
        self.peopleAtStation = random.randint(1,50)
        
    def display_info(self):
        string = f"{self.name}:\n\tLine: {self.line}\n\tBlock Number: {self.block.display_num()} \n\tLeft Door: {self.leftDoor}\n\tRight Door: {self.rightDoor}"
        return string
    
    def set_trainIn(self, x):
        self.trainIn = x
        if (x):
            numBoarding = random.randint(0,self.peopleAtStation)
            #post number of people to a train
            self.peopleAtStation -= numBoarding
            if (self.peopleAtStation < 25):
                self.peopleAtStation += random.randint(0,15)
            elif (self.peopleAtStation < 40):
                self.peopleAtStation += random.randint(0,5)
            elif (self.peopleAtStation >= 50):
                self.peopleAtStation == 50
    
    def get_trainIn(self):
        return self.trainIn
    def get_name(self):
        return self.name
