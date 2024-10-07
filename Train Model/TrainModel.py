# TrainModel.py

class TrainModel:
    def __init__(self):

        # Initialize variables
        self.commandedSpeed = 0.0
        self.currentVelocity = 0.0
        self.acceleration = 0.0
        self.authority = False
        self.power = 0.0
        self.temperature = 70.0
        self.stationName = ""
        self.emergencyBrake = False
        self.serviceBrake = False
        self.headLights = False
        self.insideLights = False
        self.advertisements = False
        self.announcements = False
        self.rightDoor = False
        self.leftDoor = False
        self.trainLength = 32.2
        self.trainWidth = 2.65
        self.trainHeight = 3.42
        self.trainMass = 40.9
        self.numberOfCars = 5
        self.crewCount = 2
        self.passCount = 0
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        # Update the UI initially
        #self.update_ui()
        self.simulate_velocity_change()

    #def update_ui(self):
        """Update the UI with the latest values."""
        #self.window.user_mode_page.update_velocity(self.currentVelocity)
        # Update other UI components similarly

    def simulate_velocity_change(self):
        """Simulate a change in velocity and update the UI."""
        self.currentVelocity += 5  # Example of changing the velocity
        #self.update_ui()

