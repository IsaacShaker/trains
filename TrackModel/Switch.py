class Switch:
    def __init__(self, line, section, number, left, right, VtoL, VtoR, LorR, IorO):
        self.line = line
        self.section = section
        self.startBlock = number
        self.vertexInOrOut = IorO
        self.leftBlock = left
        self.rightBlock = right
        self.LorR = LorR
        self.VtoL = VtoL
        self.VtoR = VtoR

    def display_info(self, index):
        if (self.LorR):
            lr = "Right"
        else:
            lr = "Left"
        string = f"Switch {index}: \n\tLine: {self.line} \n\tSection: {self.section}" + "\n\t" + f"Block Number: {self.startBlock.display_num()}\n" + "\tLeft " + f"{self.leftBlock.display_num()}\n" + "\tRight " + f"{self.rightBlock.display_num()}\n" + f"\tLeft or Right: " + lr
        return string
    
    def get_status(self):
        if (self.LorR):
            return "Right(" + str(self.rightBlock.get_num()) + ")"
        else:
            return "Left(" + str(self.leftBlock.get_num()) + ")"

    def set_L(self):
        self.LorR = False
        if self.vertexInOrOut:  #Vertex Out
            self.startBlock.set_previous_block(self.leftBlock)
            if self.VtoL:   #Vertex Out Left Opposite Direction
                self.leftBlock.set_previous_block(self.startBlock)
            else:           #Vertex Out Left Same Direction
                self.leftBlock.set_next_block(self.startBlock)
            if self.VtoR:   #Vertex Out Right Opposite Direction
                self.rightBlock.set_previous_block(None)
            else:           #Vertex Out Right Same Direction
                self.rightBlock.set_next_block(None)
        else:   #Vertex In
            self.startBlock.set_next_block(self.leftBlock)
            if self.VtoL:   #Vertex In and Left Opposite Direction
                self.leftBlock.set_next_block(self.startBlock)
            else:           #Vertex In and Left Same Direction
                self.leftBlock.set_previous_block(self.startBlock)
            if self.VtoR:   #Vertex In and Right Opposite Direction
                self.rightBlock.set_next_block(None)
            else:           #Vertex In and Right Same Direction
                self.rightBlock.set_previous_block(None)
    def set_R(self):
        self.LorR = True
        if self.vertexInOrOut:  #Vertex Out
            self.startBlock.set_previous_block(self.rightBlock)
            if self.VtoL:       #Vertex Out Left Opposite Direction
                self.leftBlock.set_previous_block(None)
            else:               #Vertex Out Left Same Direction
                self.leftBlock.set_next_block(None)
            if self.VtoR:       #Vertex Out Right Opposite Direction
                self.rightBlock.set_previous_block(self.startBlock)
            else:               #Vertex Out Right Same Direction
                self.rightBlock.set_next_block(self.startBlock)
        else:                   #Vertex In
            self.startBlock.set_next_block(self.rightBlock)
            if self.VtoL:       #Vertex In Left Opposite Direction
                self.leftBlock.set_next_block(None)
            else:               #Vertex In Left Same Direction
                self.leftBlock.set_previous_block(None)
            if self.VtoR:       #Vertex In Right Opposite Direction
                self.rightBlock.set_next_block(self.startBlock)
            else:               #Vertex In Right Same Direction
                self.rightBlock.set_previous_block(self.startBlock)

    def get_LandR(self):
        return "L: " + str(self.leftBlock.get_num()) + " R: " + str(self.rightBlock.get_num())
    def get_left_num(self):
        return self.leftBlock.get_num()
    def get_right_num(self):
        return self.rightBlock.get_num()
    def get_LorR(self):
        return self.LorR

    def change_LorR(self):
        if self.LorR:
            self.set_L()
        else:
            self.set_R()