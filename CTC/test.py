from train import Train

Train0 = Train('Train 0', 'Blue', 'Station B')

new_authority = 50

Train0.setAuthority(new_authority)

print(Train0.name, 'is going to', Train0.destination, 'with authority', Train0.authority,'m!')