from PyQt6.QtCore import QTimer, QObject
from threading import Thread, Event
import time
import importlib.util
import os

class PLCManager(QObject):
    def __init__(self, data, line, mode, auto, plc_num):
        super().__init__()
        self.plc_thread = None
        self.stop_event = Event()  # Event to signal when to stop the PLC thread
        self.update_data_timer = QTimer()  # Create a QTimer instance
        self.module_name = ""

        self.track_data = data[line][mode]
        self.auto = auto
        self.plc_num = plc_num

        self.plc_module = None

        # create the inputs that are going into PLC
        self.num_blocks = 0
        self.num_switches = 0
        self.num_crossings = 0
        self.num_traffic_lights = 0

        if line == "Green":
            self.num_blocks = 151 # extra is for YARD
            self.num_switches = 6
            self.num_crossings = 2
            self.num_traffic_lights = 10
        elif line == "Red":
            self.num_blocks = 77 # extra is for YARD
            self.num_switches = 7
            self.num_crossings = 2
            self.num_traffic_lights = 10
        if line == "Blue":
            print("Blue Line PLC")
            self.num_blocks = 16
            self.num_switches = 1 # extra is for YARD
            self.num_traffic_lights = 3
            self.num_crossings = 1
        
        self.blocks = [False] * self.num_blocks
        self.switch_suggest = [False] * self.num_switches

        # create the outputs that going out of PLC
        self.speed_hazard = [False] * self.num_blocks
        self.switches = [False] * self.num_switches
        self.crossings = [False] * self.num_crossings
        self.traffic_lights = [False] * self.num_traffic_lights

        self.update_input_data()

        self.update_data_timer.timeout.connect(self.update_data)

    def update_auto(self, auto):
        self.auto = auto

    def start_updating_timer(self):
        """Start the timer to update input data every 100 milliseconds. Similar to Systick interupt."""
        self.update_data_timer.start(100)  # 100 milliseconds

    def stop_updating_timer(self):
        """Stop the timer."""
        self.update_data_timer.stop()

    def update_data(self):
        self.update_input_data()
        if self.plc_module is not None:
            self.plc_module.main(self.stop_event, self.blocks, self.switch_suggest, self.switches, self.traffic_lights, self.crossings, self.speed_hazard)
        self.update_output_data()

    def update_input_data(self):        
        # populate the list with proper values
        for block in self.track_data["blocks"]:
            self.blocks[block["block"]] = block["occupied"]
            self.speed_hazard[block["block"]] = block["speed_hazard"]
        
        for switch in self.track_data["switches"]:
            self.switch_suggest[switch["id"]] = switch["suggested_toggle"]

    def update_output_data(self):
        # don't update if user is in manual mode
        if self.auto == False:
            return

        # push PLC outputs to track_data that is shared with the UI
        for block in self.track_data["blocks"]:
            block["speed_hazard"] = self.speed_hazard[block["block"]]

        for switch in self.track_data["switches"]:
            if switch["plc_num"] == self.plc_num:
                switch["toggled"] = self.switches[switch["id"]]

        for crossing in self.track_data["crossings"]:
            if crossing["plc_num"] == self.plc_num:
                crossing["toggled"] = self.crossings[crossing["id"]]

        for light in self.track_data["traffic_lights"]:
            if light["plc_num"] == self.plc_num:
                light["toggled"] = self.traffic_lights[light["id"]]
    
    def run_plc(self, plc_module):
        """Run the PLC logic in a thread."""
        while not self.stop_event.is_set():
            # Call the main function or loop inside the uploaded PLC
            try:
                print(self.module_name + " program uploaded and running.")
                plc_module.main(self.stop_event, self.blocks, self.switch_suggest, self.switches, self.traffic_lights, self.crossings, self.speed_hazard)  # Assuming the PLC file has a 'main' function
            except Exception as e:
                print(f"Error running PLC: {e}")
            time.sleep(0.1)  # Add a sleep to prevent CPU hogging

    def stop_current_plc(self):
        """Stop the currently running PLC."""
        if self.plc_thread and self.plc_thread.is_alive():
            self.stop_event.set()  # Signal the thread to stop
            self.plc_thread.join()  # Wait for the thread to stop
            self.stop_event.clear()  # Reset the event for future use
            print(self.module_name + " program successfully stopped. ")
        self.stop_updating_timer()  # Stop the updating timer

    def start_new_plc(self, plc_filepath):
        """Upload and start a new PLC program."""
        self.stop_current_plc()  # Stop the previous PLC
        
        # Dynamically load the new PLC module
        self.plc_module = self.load_plc_module(plc_filepath)
        
        # Start a new thread with the new PLC program
        # self.plc_thread = Thread(target=self.run_plc, args=(self.plc_module,))
        # self.plc_thread.start()
        # self.start_updating_timer()  # Start updating inputs for the new PLC

    def load_plc_module(self, filepath):
        """Dynamically load a Python file as a module."""
        self.module_name = os.path.basename(filepath)
        print("Module Name: " + self.module_name)
        spec = importlib.util.spec_from_file_location(self.module_name, filepath)
        plc_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plc_module)
        return plc_module