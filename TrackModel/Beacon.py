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
    
    def get_table_data(self, index):
        if index == 0:
            return self.section
        if index == 1:
            return self.block
        if index == 2:
            return self.staticData
