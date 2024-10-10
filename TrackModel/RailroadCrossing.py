class RailroadCrossing:
    def __init__(self, line, section, block, UorD):
        self.line = line
        self.section = section
        self.block = block
        self.UorD = UorD

    def display_info(self, index):
        if (self.UorD):
            ud = "Down"
        else:
            ud = "Up"
        string = f"Railroad Crossing {index}:\n\tLine: {self.line} \n\tSection: {self.section}" + "\n\t" + f"Block Number: {self.block.display_num()}" + f"\n\tUp or Down: " + ud
        return string

    def get_UorD(self):
        return self.UorD

    def set_U(self):
        self.UorD = False

    def set_D(self):
        self.UorD = True