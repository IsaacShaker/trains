from PyQt6.QtCore import QTimer, QObject, QTime
import requests

URL = 'http://127.0.0.1:5000'

class World_Clock(QObject):
    def __init__(self):
        super().__init__()
        
        # Initialize hour, minute, and second variables
        self.clock_activated = False
        self.hour = 6
        self.minute = 0
        self.seconds = 0
        self.seconds_cum = 0
        self.sim_speed = 1
        self.time_string = "00:00:00"
        self.pause = False

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
        if self.clock_activated and not self.pause:
            self.seconds += 1
            self.seconds_cum += 1

            if self.seconds >= 60:
                self.second = 0
                self.minute += 1

            if self.minute >= 60:
                self.minute = 0
                self.hour += 1

            if self.hour >= 24:
                self.hour = 0

            self.time_string = (f"{self.hour:02d}:{self.minute:02d}:{self.seconds:02d}")

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
        self.sim_speed = input
        
        if self.sim_speed != 0:
            if not self.pause:
                self.start_timer()
            self.pause = False
            self.timer.setInterval(int(1000 / self.sim_speed))
        else:
            self.pause_timer()

    def set_clock_activated(self, input):
        self.clock_activated = input

    def start_timer(self):
        self.timer.start()

    def pause_timer(self):
        self.timer.stop()
        self.pause = True