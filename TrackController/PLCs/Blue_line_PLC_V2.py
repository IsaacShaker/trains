import time

def main(stop_event, block_occupancies, switch_suggestions, switches, traffic_lights, crossings): # block_occupancy_bools, switch_position_bools, speed_bool, plc_outputs, plc_output_lock
    """Main loop of the PLC program that processes inputs and updates outputs."""
    while not stop_event.is_set():
        print("Running Dummy PLC")
        # Simulate delay to avoid CPU hogging
        time.sleep(3)
