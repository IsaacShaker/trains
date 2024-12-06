import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings, speed_hazard):
    """Main loop of the PLC program that processes inputs and updates outputs."""
    # define some functions to make it more readable:
    def N_occupied():
        for i in range(77, 86):
            if block_occupancies[i]:
                return True
        return False
    
    def Q_occupied():
        for i in range(98, 101):
            if block_occupancies[i]:
                return True
        return False
    
    def M_occupied():
        for i in range(74, 77):
            if block_occupancies[i]:
                return True
        return False
    
    def set_Q_hazard(truth_val):
        for i in range(98, 101):
            speed_hazard[i] = truth_val
    
    def set_M_hazard(truth_val):
        for i in range(74, 77):
            speed_hazard[i] = truth_val

    def Q_is_hazard():
        for i in range(98, 101):
            if speed_hazard[i]:
                return True
        return False
    
    def M_is_hazard():
        for i in range(74, 77):
            if speed_hazard[i]:
                return True
        return False
    
    while not stop_event.is_set():
        # reset speed hazard
        for i in range(len(speed_hazard)):
            speed_hazard[i] = False

        # Sections I - M
        for i in range(36, 77):
            if block_occupancies[i]:
                # trailing 4 blocks so other trains don't get too close
                for j in range(1, 5):
                    speed_hazard[i-j] = True
<<<<<<< HEAD
       
=======
        
        # Sections O - Q
        for i in range(86, 101):
            if block_occupancies[i]:
                # trailing 4 blocks so other trains don't get too close
                for j in range(1, 5):
                    speed_hazard[i-j] = True

        # Sections S -  U
        for i in range(105, 117):
            if block_occupancies[i]:
                # trailing 4 blocks so other trains don't get too close
                for j in range(1, 5):
                    speed_hazard[i-j] = True
>>>>>>> mtm
        
        if N_occupied() == False:
            switches[4] = False
            switches[5] = True
            traffic_lights[6] = True
            traffic_lights[7] = False
            traffic_lights[8] = True
            traffic_lights[9] = False

            set_Q_hazard(False)
            set_M_hazard(False)

            # if trains are at both ends of section N, give priority over trains at section M
            if Q_occupied() and M_occupied():
                set_Q_hazard(True) # stops trains at Q
        elif N_occupied() == True and not block_occupancies[78] and not block_occupancies[100]:
            switches[4] = True
            switches[5] = False
            traffic_lights[6] = False
            traffic_lights[7] = True
            traffic_lights[8] = False
            traffic_lights[9] = True

            # stop other trains from entering section N
            set_M_hazard(True)
            set_Q_hazard(True)

        # check 3 blocks behind crossing and block of crossing (4 total blocks)
        crossings[1] = False # Default is up
        for i in range(4):
            if block_occupancies[108 - i]: # block 108 is the railroad crossing
                crossings[1] = True # Put the crossing down

        # Simulate delay to avoid CPU hogging
        time.sleep(0.1)
