import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings): # block_occupancy_bools, switch_position_bools, speed_bool, plc_outputs, plc_output_lock
    """Main loop of the PLC program that processes inputs and updates outputs."""
    while not stop_event.is_set():
        
        # logic to control crossing
        if block_occupancies[0] or block_occupancies[1] or block_occupancies[2]:
            # print("set crossing down")
            crossings[0] = True
        else:
            # print("set crossing up")
            crossings[0] = False

        # logic to control switch

        # if there is a train on the switch block, the switch suggestion is from 5 to 6, and section B is clear, then set the switch to the switch suggestion and turn light green
        if block_occupancies[4]:
            if switch_suggestions[0] == False:
                if not(block_occupancies[6] or block_occupancies[7] or block_occupancies[8] or block_occupancies[9]):
                    switches[0] = False
                    traffic_lights[0] = True
                    traffic_lights[1] = False

                elif not(block_occupancies[11] or block_occupancies[12] or block_occupancies[13] or block_occupancies[14]):
                    print("avoiding collision in section B detour to section C for safety purposes")
                    switches[0] = True
                    traffic_lights[0] = False
                    traffic_lights[1] = True

                else:
                    print("Both sections B and C have trains, pray to god your brakes are working")
                    traffic_lights[0] = False
                    traffic_lights[1] = False

            elif switch_suggestions[0] == True:
                if not(block_occupancies[11] or block_occupancies[12] or block_occupancies[13] or block_occupancies[14]):
                    switches[0] = True
                    traffic_lights[0] = False
                    traffic_lights[1] = True

                elif not(block_occupancies[6] or block_occupancies[7] or block_occupancies[8] or block_occupancies[9]):
                    print("avoiding collision in section C detour to section B for safety purposes")
                    switches[0] = False
                    traffic_lights[0] = True
                    traffic_lights[1] = False

                else:
                    print("Both sections B and C have trains, pray to god your brakes are working")
                    traffic_lights[0] = False
                    traffic_lights[1] = False

        # Simulate delay to avoid CPU hogging
        time.sleep(0.1)
