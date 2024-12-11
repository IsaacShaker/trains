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
        return "Blocks: " + nums + "\nOccupied Blocks: " + occ_nums + "\nClosed: " + mc_nums+ "\nBroken Track: " + btf_nums + "\nTrack Circuit Failure: " + tcf_nums + "\nPower Failure: " + pf_nums + "\nBlock Heaters: " + bh_nums
    
    def check_occupied(self):
        self.occupied = any(block.get_if_train() for block in self.blocks)

    def get_occupied(self):
        return self.occupied