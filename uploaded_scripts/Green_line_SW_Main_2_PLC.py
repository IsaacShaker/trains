import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings, speed_hazard):
    """Main loop of the PLC program that processes inputs and updates outputs."""
    def set_J_hazard(truth_val):
        for i in range(58, 63):
            speed_hazard[i] = truth_val
        
    while not stop_event.is_set():
        # We want to pull out of the YARD
        if switch_suggestions[3] == False and block_occupancies[62] == False and block_occupancies[61] == False and block_occupancies[60] == False:
            switches[3] = False
            speed_hazard[0] = False
            set_J_hazard(True)
            traffic_lights[5] = False
        else:
            switches[3] = True
            speed_hazard[0] = True
            set_J_hazard(False)
            traffic_lights[5] = True
        
        break
        # Simulate delay to avoid CPU hogging
        time.sleep(0.1)
