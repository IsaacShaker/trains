class Station:
    def __init__(self, name, line, section, number, LandR, LorR):
        self.name = name
        self.line = line
        self.section = section
        self.block = number
        self.LandR = LandR
        self.LorR = LorR
        
    def display_info(self):
        string = f"{self.name}:\n\tLine: {self.line} \n\tSection: {self.section} \n\tBlock Number: {self.block.display_num()} \n\tLeft and Right: {self.LandR}\n\tLeft or Right: {self.LorR}"
        return string
