from train import Train
from TrackController import TrackController

Train0 = Train('Train 0', 'Blue', 'STATION: B', 3)

wayside = TrackController(Train0)

switch = wayside.change_switch()

if switch == True:
    print(Train0.name, 'is going to Station B')
else:
    print(Train0.name, 'is going to Station C')