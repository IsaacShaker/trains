from PyQt6.QtCore import QTimer, QObject, QTime
import requests

URL = 'http://127.0.0.1:5000'

class World_Clock(QObject):
    def __init__(self):
        super().__init__()
        
        # Initialize hour, minute, and second variables
        self.clock_activated = False
        self.hour = 7
        self.minute = 30
        self.seconds = 0
        self.seconds_cum = 1 * 60 * 60 * 7 + (1 * 60 * 30) 
        self.sim_speed = 1
        self.interval = 1000
        self.time_string = "00:00:00"
        self.counter = 0

        # Create a QTimer that triggers every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 ms = 1 second

        self.clock_dict = {
            "seconds": self.seconds,
            "seconds_cum": self.seconds_cum,
            "minute": self.minute,
            "hour": self.hour,
            "time_string": self.time_string
        }

    def update_time(self):
        """Updates the clock variables to simulate a military time clock."""
        if self.clock_activated and self.sim_speed != 0:

            #self.seconds += 1 *self.sim_speed
            self.seconds_cum += 1 *self.sim_speed
            self.seconds = self.seconds_cum % 60

            minute_cum = self.seconds_cum // 60
            self.minute = minute_cum % 60

            hours_cum = minute_cum // 60
            self.hour = hours_cum % 24
            '''
            if self.seconds >= 60:
                self.second = 0
                self.minute += 1

            if self.minute >= 60:
                self.minute = 0
                self.hour += 1

            if self.hour >= 24:
                self.hour = 0
            '''
            self.time_string = (f"{self.hour:02d}:{self.minute:02d}:{self.seconds:02d}")
            #print(f"WORLD CLOCK: {self.time_string}")

            self.clock_dict["seconds_cum"] = self.seconds_cum
            self.clock_dict["seconds"] = self.seconds
            self.clock_dict["minute"] = self.minute
            self.clock_dict["hour"] = self.hour
            self.clock_dict["time_string"] = self.time_string
            response = requests.post(URL + "/global/get-world-clock", json=self.clock_dict)
            

    def get_hour(self):
        """Return the current hour."""
        return self.hour

    def get_minute(self):
        """Return the current minute."""
        return self.minute

    def get_second(self):
        """Return the current second."""
        return self.second
    
    def get_second(self):
        return self.seconds_cum
    
    def get_time_string(self):
        return self.time_string

    def set_sim_speed(self, input):
        #print(f"SIM SPEED IN WORLD CLOCK: {self.sim_speed}")    
        if input != 0:
            self.sim_speed = input
            #self.interval = 1000/self.sim_speed
            #self.timer.setInterval(int(self.interval))
        
            #if not self.timer.isActive():
            #    self.timer.start(int(self.interval))

    def set_clock_activated(self, input):
        self.clock_activated = input

    def start_timer(self):
        self.timer.start()

    def pause_timer(self):
        self.timer.stop()

        
