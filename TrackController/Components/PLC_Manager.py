from PyQt6.QtCore import QTimer, QObject
from threading import Thread, Event
import time
import importlib.util
import os

class PLCManager(QObject):
    def __init__(self, data, auto):
        super().__init__()
        self.plc_thread = None
        self.stop_event = Event()  # Event to signal when to stop the PLC thread
        self.update_input_timer = QTimer()  # Create a QTimer instance
        self.update_output_timer = QTimer()
        self.module_name = ""

        self.track_data = data
        self.auto = auto

        # create the inputs that are going into PLC
        self.blocks = []
        self.switch_suggest = []

        # create the outputs that going out of PLC
        self.switches = []
        self.crossings = []
        self.traffic_lights = []

        self.update_input_data()
        self.create_output_data()

        self.update_input_timer.timeout.connect(self.update_input_data)
        self.update_output_timer.timeout.connect(self.update_output_data)

    def update_auto(self, auto):
        self.auto = auto

        for i, switch in enumerate(self.track_data["switches"]):
            self.switches[i] = switch["toggled"]
        
        for i, crossing in enumerate(self.track_data["crossings"]):
            self.crossings[i] = crossing["toggled"]
        
        for i, light in enumerate(self.track_data["traffic_lights"]):
            self.traffic_lights[i] = light["toggled"]

    def start_updating_timer(self):
        """Start the timer to update input data every 100 milliseconds. Similar to Systick interupt."""
        self.update_input_timer.start(100)  # 100 milliseconds
        self.update_output_timer.start(100)

    def stop_updating_timer(self):
        """Stop the timer."""
        self.update_input_timer.stop()
        self.update_output_timer.stop()

    def update_input_data(self):
        # clear the lists
        self.blocks.clear()
        self.switch_suggest.clear()
        
        # populate the list with proper values
        for block in self.track_data["blocks"]:
            self.blocks.append(block["occupied"])
        
        for switch in self.track_data["switches"]:
            self.switch_suggest.append(switch["suggested_toggle"])

    def update_output_data(self):
        # don't update if user is in manual mode
        if self.auto == False:
            return

        # push PLC outputs to track_data that is shared with the UI
        for i, switch_state in enumerate(self.switches):
            self.track_data['switches'][i]["toggled"] = switch_state
        
        for i, crossing_state in enumerate(self.crossings):
            self.track_data['crossings'][i]["toggled"] = crossing_state

        for i, light_state in enumerate(self.traffic_lights):
            self.track_data['traffic_lights'][i]["toggled"] = light_state

    def create_output_data(self):
        self.switches.clear()
        self.crossings.clear()
        self.traffic_lights.clear()

        for switch in self.track_data["switches"]:
            self.switches.append(switch["toggled"])
        
        for crossing in self.track_data["crossings"]:
            self.crossings.append(crossing["toggled"])
        
        for light in self.track_data["traffic_lights"]:
            self.traffic_lights.append(light["toggled"])
    
    def run_plc(self, plc_module):
        """Run the PLC logic in a thread."""
        while not self.stop_event.is_set():
            # Call the main function or loop inside the uploaded PLC
            try:
                print(self.module_name + " program uploaded and running.")
                plc_module.main(self.stop_event, self.blocks, self.switch_suggest, self.switches, self.traffic_lights, self.crossings)  # Assuming the PLC file has a 'main' function
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
        plc_module = self.load_plc_module(plc_filepath)
        
        # Start a new thread with the new PLC program
        self.plc_thread = Thread(target=self.run_plc, args=(plc_module,))
        self.plc_thread.start()
        self.start_updating_timer()  # Start updating inputs for the new PLC

    def load_plc_module(self, filepath):
        """Dynamically load a Python file as a module."""
        self.module_name = os.path.splitext(os.path.basename(filepath))[0]
        print("Module Name: " + self.module_name)
        spec = importlib.util.spec_from_file_location(self.module_name, filepath)
        plc_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plc_module)
        return plc_module