class Clock:

    def __init__(self):
        self.sim_speed = 1.00  # speed of the simulation
        self.elapsed_time = 0  # time elapsed in seconds
        self.current_time = ''  # current time formatted
        self.simulation_running = False  # status of the simulation
        self.old_time = 0  # initialize oldTime to track time

    # Format the time to the form of a clock
    def format_time(self, seconds: int):
        self.current_time = ''
        hours = int(seconds // 3600) % 24
        minutes = int(seconds % 3600) // 60
        seconds = int(seconds % 60)
        self.current_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        return self.current_time
    
    # Update the clock every real-time second that passes
    def update_clock(self):
        # Only update the clock if the simulation is running
        if self.simulation_running:
            # Update the time according to the previous time and the simulation speed
            self.new_time = self.old_time + (1 * self.sim_speed)
            self.current_time = self.format_time(self.new_time)

            # Update oldTime to the newTime for the next call
            self.old_time = self.new_time
        return self.old_time
    
    def get_sim_speed(self):
        return self.sim_speed