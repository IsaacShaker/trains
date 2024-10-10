class Station:
    def __init__(self, name, line, section, number, Left, Right):
        self.name = name
        self.line = line
        self.section = section
        self.block = number
        self.leftDoor = Left
        self.rightDoor = Right
        
    def display_info(self):
        string = f"{self.name}:\n\tLine: {self.line} \n\tSection: {self.section} \n\tBlock Number: {self.block.display_num()} \n\tLeft Door: {self.leftDoor}\n\tRight Door: {self.rightDoor}"
        return string
