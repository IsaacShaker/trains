class TrafficLight:
    def __init__(self, line, section, block, RorG):
        self.line = line
        self.section = section
        self.block = block
        self.RorG = RorG

    def display_info(self, index):
        if (self.RorG):
            rg = "Green"
        else:
            rg = "Red"
        string = f"Traffic Light {index}: \n\tLine: {self.line} \n\tSection: {self.section}" + "\n\t" + f"Block Number: {self.block.display_num()}" + f"\n\tRed or Green: " + rg
        return string
    
    def get_status(self):
        if (self.RorG):
            return "Green"
        else:
            return "Red"
    def get_RorG(self):
        return self.RorG
    
    def set_R(self):
        self.RorG = False
    def set_G(self):
        self.RorG = True
