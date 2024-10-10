from train import Train
import time

class TrackController:
    def __init__(self):
        self.switch_status = True
        self.train = Train('Train0', 'Blue', 'STATION: B', 3)
        #self.occupied_blocks = []

    def change_switch(self):
        print('in change_switch')
        if self.train.destination == 'STATION: B':
            print('in true case')
            self.switch_status = True # Switch is on top track
            return self.switch_status
        else:
            print('in false case')
            self.switch_status = False #Switch is on lower track
            return self.switch_status
        
    def send_occupancies(self):
        self.occupied_block = ('Blue', 1)
        return self.occupied_block
    
    #def simulate_train(self, time):
        