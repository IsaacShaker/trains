class Section:
    def __init__(self, name):
        self.name = name
        self.blocks = []
        self.occupied = False

    def add_block(self, block):
        self.blocks.append(block)

    def display_info(self):
        nums = ''
        occ_nums = ''
        btf_nums = ''
        tcf_nums = ''
        pf_nums = ''
        bh_nums = ''
        mc_nums = ''
        string = ''
        for i, block in enumerate(self.blocks):  # Use enumerate for both index and item
            tempNum = str(block.get_num())  # block is the object
            nums += (tempNum + " ")
            if block.get_if_train():
                occ_nums += (tempNum + " ")
            if block.get_closed():
                mc_nums += (tempNum + " ")
            if block.get_broken():
                btf_nums += (tempNum + " ")
            if block.get_circuit():
                tcf_nums += (tempNum + " ")
            if block.get_power():
                pf_nums += (tempNum + " ")
            if block.get_heater():
                bh_nums += (tempNum + " ")
        string += "Blocks: " + nums
        if (len(occ_nums) > 0):
            string += "\nOccupied Blocks: " + occ_nums
        if (len(mc_nums) > 0): 
            string += "\nClosed: " + mc_nums
        if (len(btf_nums) > 0): 
            string += "\nBroken Track: " + btf_nums
        if (len(tcf_nums) > 0): 
            string += "\nTrack Circuit Failure: " + tcf_nums
        if (len(pf_nums) > 0):
            string += "\nPower Failure: " + pf_nums
        if (len(bh_nums) > 0):
            string += "\nBlock Heaters: " + bh_nums

        return string
    
    def check_occupied(self):
        self.occupied = any(block.get_if_train() for block in self.blocks)

    def get_occupied(self):
        return self.occupied