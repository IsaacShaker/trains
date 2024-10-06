from TrainModel_UI import MainWindow

class TrainModel:
    # Class variable to hold all train models
    train_models = []

    def __init__(self):
        self.ID = ID  # Unique identifier for each train model
        # Create an instance of MainWindow
        self.window = MainWindow()

        # Initialize variables (as you've defined previously)
        self.commandedSpeed = 0.0
        self.currentVelocity = 0.0
        self.acceleration = 0.0
        self.authority = False
        self.power = 0.0
        self.temp = 70.0
        self.stationName = ""
        self.emergencyBrake = False
        self.serviceBrake = False
        self.headLights = False
        self.insideLights = False
        self.advertisements = False
        self.announcements = False
        self.doors = False
        self.doorSide = DoorSide.SIDE_RIGHT
        self.trainLength = 32.2
        self.trainWidth = 2.65
        self.trainHeight = 3.42
        self.trainMass = 40.9
        self.trainCrewCount = 2
        self.trainPassCount = 0
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        # Add this instance to the list of train models
        TrainModel.train_models.append(self)

        # Update the UI initially
        self.update_ui()
        self.simulate_velocity_change()

    def update_ui(self):
        """Update the UI with the latest values."""
        self.window.user_mode_page.update_velocity(self.currentVelocity)
        # Update other UI components similarly

    def simulate_velocity_change(self):
        """Simulate a change in velocity and update the UI."""
        self.currentVelocity += 5  # Example of changing the velocity
        self.update_ui()
