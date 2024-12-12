import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings, speed_hazard):
    """Main loop of the PLC program that processes inputs and updates outputs."""

    def ABCDEF_occupied():
        for i in range(1, 29):
            if block_occupancies[i]:
                return True
        return False
    
    def DEF_occupied():
        for i in range(13, 29):
            if block_occupancies[i]:
                return True
        return False
    
    def A_occupied():
        for i in range(1, 4):
            if block_occupancies[i]:
                return True
        return False
    
    def YorZ_occupied():
        for i in range(147, 151):
            if block_occupancies[i]:
                return True
        return False
    
    def set_A_hazard(truth_val):
        for i in range(1, 4):
            speed_hazard[i] = truth_val

    def set_YorZ_hazard(truth_val):
        for i in range(147, 151):
            speed_hazard[i] = truth_val
    
    while not stop_event.is_set():
        # A through C
        for i in range(1, 13):
            if block_occupancies[i]:
                # trailing 4 blocks so other trains don't get too close
                for j in range(1, 5):
                    speed_hazard[i-j] = True
            speed_hazard[i] = False

        # Sections V - Z
        for i in range(117, 151):
            if block_occupancies[i]:
                # trailing 4 blocks so other trains don't get too close
                for j in range(1, 5):
                    speed_hazard[i-j] = True
            speed_hazard[i] = False
    
        if ABCDEF_occupied() == False:
            switches[0] = False
            switches[1] = True
            traffic_lights[0] = False
            traffic_lights[1] = True
            traffic_lights[2] = False
            traffic_lights[3] = True

            #set_A_hazard(False)
            set_YorZ_hazard(False)

            # if trains are at both ends of section DEF, give priority over trains at section Z
            #if A_occupied() and YorZ_occupied():
                #set_A_hazard(True) # stops trains at A
        elif (DEF_occupied() == False and not block_occupancies[150]) or ABCDEF_occupied() == True:
            #switches[0] = True
            switches[1] = False
            #traffic_lights[0] = True
            #traffic_lights[1] = False
            traffic_lights[2] = True
            traffic_lights[3] = False
            set_YorZ_hazard(True)

            if DEF_occupied() == True and not block_occupancies[1]:
                switches[0] = False
                traffic_lights[0] = False
                traffic_lights[1] = True

            elif DEF_occupied() == False:
                switches[0] = True
                traffic_lights[0] = True
                traffic_lights[1] = False


            # stop other trains from entering section
            #set_YorZ_hazard(True)
            #set_A_hazard(True)


        # check 3 blocks behind crossing and block of crossing (4 total blocks)
        crossings[0] = False # Default is up
        for i in range(4):
            if block_occupancies[19 - i]: # block 19 is the railroad crossing
                crossings[0] = True # Put the crossing down
                break
            if block_occupancies[19 + i]: # block 19 is the railroad crossing
                crossings[0] = True # Put the crossing down
                break

        # Simulate delay to avoid CPU hogging
        break
        time.sleep(0.1)

