class Block():
    def __init__(self, line, number, speed):
        self.block_line = line
        self.block_number = number
        self.block_speed = speed

    def get_block_line(self):
        return self.block_line
    
    def get_block_number(self):
        return self.block_number
    
    def get_block_speed(self):
        return self.block_speed
    