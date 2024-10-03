class Switch:
    def __init__(self, line, section, number, left, right, LorR):
        self.line = line
        self.section = section
        self.startBlock = number
        self.leftBlock = left
        self.rightBlock = right
        self.LorR = LorR

    def display_info(self, index):
        if (self.LorR):
            lr = "Right"
        else:
            lr = "Left"
        string = f"Switch {index}: \n\tLine: {self.line} \n\tSection: {self.section}" + "\n\t" + f"Block Number: {self.startBlock.display_num()}\n" + "\tLeft " + f"{self.leftBlock.display_num()}\n" + "\tRight " + f"{self.rightBlock.display_num()}\n" + f"\tLeft or Right: " + lr
        return string
    
    def get_LorR(self):
        return self.LorR
    
    def change_LorR(self):
        if(self.LorR):
            self.LorR = False
            self.startBlock.set_next_block(self.leftBlock)
        else:
            self.LorR = True
            self.startBlock.set_next_block(self.rightBlock)
    
    def set_L(self):
        self.LorR = False
        self.startBlock.set_next_block(self.leftBlock)
    
    def set_R(self):
        self.LorR = True
        self.startBlock.set_next_block(self.rightBlock)