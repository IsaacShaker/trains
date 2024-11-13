import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings, speed_hazard):
    """Main loop of the PLC program that processes inputs and updates outputs."""
    def set_J_hazard(truth_val):
        for i in range(58, 63):
            speed_hazard[i] = truth_val
        
    while not stop_event.is_set():
        # Pull into the YARD
        if switch_suggestions[2] == False and block_occupancies[58] == False:
            switches[2] = False
            traffic_lights[4] = True
        else:
            switches[2] = True
            traffic_lights[4] = False
        

        # We want to pull out of the YARD
        if switch_suggestions[3] == True and block_occupancies[63] == False:
            switches[3] = True
            speed_hazard[0] = False
            set_J_hazard(True)
            traffic_lights[5] = False
        else:
            switches[3] = False
            speed_hazard[0] = True
            set_J_hazard(False)
            traffic_lights[5] = True
        
        # Simulate delay to avoid CPU hogging
        time.sleep(0.1)
