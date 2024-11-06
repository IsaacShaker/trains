class Beacon:
    def __init__(self, line, section, block, staticData):
        self.line = line
        self.section = section
        self.block = block
        self.staticData = staticData
        
    def display_info(self):
        string = f"Beacon: \n\tLine: {self.line} \n\tSection: {self.section} \n\tBlock Number: {self.block.display_num()} \n\tStatic Data: {self.staticData}"
        return string
    
    def get_staticData(self):
        return self.staticData
