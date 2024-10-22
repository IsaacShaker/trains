import time
from clock import Clock  # Assuming your class is saved in a file named clock.py

class TestClock(Clock):
    def __init__(self):
        super().__init__()

    def run_simulation(self, total_seconds: int):
        # Start the simulation
        self.simulation_running = True

        for _ in range(total_seconds):
            if (_ == 3):
                self.sim_speed = 10
            
            if (_ == 5):
                self.sim_speed = 50

            if (_ == 8):
                self.sim_speed = 1

            time.sleep(1)  # Wait for 1 second in real-time
            self.update_clock()  # Update the clock
            print(self.current_time)  # Print the updated time

        # Stop the simulation after the loop ends
        self.simulation_running = False

# Create an instance of TestClock and run the simulation for 10 seconds
if __name__ == "__main__":
    clock = TestClock()
    clock.run_simulation(10)
