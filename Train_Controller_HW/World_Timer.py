from PyQt6.QtCore import QTimer, QObject, QTime
import requests

URL = 'http://127.0.0.1:5000'

class World_Clock(QObject):
    def __init__(self):
        super().__init__()
        
        # Initialize hour, minute, and second variables
        self.hour = 0
        self.minute = 0
        self.seconds = 0
        self.seconds_cum = 0
        self.sim_speed = 1

        # Create a QTimer that triggers every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 ms = 1 second

        self.clock_dict = {
            "seconds": self.seconds,
            "seconds_cum": self.seconds_cum,
            "minute": self.minute,
            "hour": self.hour
        }

    def update_time(self):
        """Update the clock variables to simulate a military time clock."""
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

        self.clock_dict["seconds_cum"] = self.seconds_cum
        self.clock_dict["seconds"] = self.seconds
        self.clock_dict["minute"] = self.minute
        self.clock_dict["hour"] = self.hour
        response = requests.post(URL + "/train-controller/get-world-clock", json=self.clock_dict)

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
    
    def set_sim_speed(self, input):
        self.sim_speed = input
        
        self.timer.setInterval(int(1000 / self.sim_speed))