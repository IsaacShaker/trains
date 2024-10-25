from scheduleReader import ScheduleReader

myReader = ScheduleReader()

trains = []

trains = myReader.get_green_routes()

for train in trains:
    print(train.name, 'Authorities:')
    print(train.route_authorities)
    print('-----------------------------------------------------------------------------------------------')