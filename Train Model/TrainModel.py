# TrainModel.py

import time

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
        self.maxOccupancy=222
        self.person_weight_pounds=150
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        # Update the UI initially
        #self.update_ui()
        #self.simulate_velocity_change()

    # #def update_ui(self):
    #     """Update the UI with the latest values."""
    #     #self.window.user_mode_page.update_velocity(self.currentVelocity)
    #     # Update other UI components similarly

    # def simulate_velocity_change(self):
    #     """Simulate a change in velocity and update the UI."""
    #     self.currentVelocity += 5  # Example of changing the velocity
    #     #self.update_ui()

    def adjust_temperature(self, target_temperature):
        while abs(self.temperature - target_temperature) > 0.1:
            # First-order differential equation update
            self.temperature += .1 * (target_temperature - self.temperature)

            # Simulate time passage (you can adjust the sleep duration)
            time.sleep(0.1)  # Sleep for 100ms for a smoother transition
            print(f"Current Temperature: {self.temperature:.2f}°C")

        print("Target temperature reached.")

    def calculate_total_mass(self):
    
        # Convert train weight to pounds
        train_weight_pounds = self.trainMass * 2000
        
        # Calculate total weight of crew and passengers
        total_people_weight = (self.crewCount + self.passCount) * self.person_weight_pounds
        
        # Total weight in pounds
        total_weight_pounds = train_weight_pounds + total_people_weight
        
        # Convert total weight to tons
        total_weight_tons = total_weight_pounds / 2000  # Convert back to tons

        print ({total_weight_tons})

        trainMass=total_weight_tons
        
        return total_weight_tons

    # def travelled_dist(self):
    #     total_vel = (self.lastVel + self.currVel) / 2  # Average velocity
    #     dist = self.lastPos + (self.elapsedTime / 2) * total_vel  # Distance calculation
    #     return dist

    # def calc_velocity(self):
    #     """Calculate average velocity from the last loop."""
    #     total_acc = (self.lastAccel + self.currAccel) / 2  # Average acceleration
    #     vel = self.lastVel + (self.elapsedTime / 2) * total_acc  # Velocity calculation

    #     # Limit so that if velocity calculation is less than 0, it is = 0
    #     if vel < 0:
    #         vel = 0
    #     if self.lastVel <= 0 and (self.serviceBrake or self.emergencyBrake):
    #         vel = 0

    #     return vel

    def limit_force(self):
        max_force = self.trainMass * 0.5
        #If our force passes the max allowed
        if self.currForce > max_force:
            self.currForce = max_force
        #If the power is at 0 and we are not moving or the emergency brake is pulled
        elif (self.currPower == 0 and self.lastVel == 0) or self.emergencyBrake:
            self.currForce = 0
        #If the train is not moving, add limiter so the force is not infinite
        elif self.lastVel == 0:
            self.currForce = max_force

    def limit_accel(self):
        #If we have a failure status, physics based decleration
        if self.failureStatus == 3 and (self.serviceBrake or self.emergencyBrake):
            self.currAccel = (self.currForce - (0.01 * self.mass * 9.8)) / self.mass
            self.serviceBrake = False
            self.emergencyBrake = False
        #If the power command is 0 and we are not moving, brake case
        elif self.currPower == 0 and self.currVel > 0:
            #2.73 for emergency, 1.2 for service
            self.currAccel = -2.73 if self.emergencyBrake else -1.2
        #Limit acceleration if there is power
        elif self.currPower != 0:
            if self.currAccel > 0.5:
                self.currAccel = 0.5
        #Otherwise we are at a constant speed
        else:
            self.currAccel = 0

    def update_passengers(self):
        # If the doors are open and the train was not at a station in the previous loop
        # if (self.controls['doorLeftOpen'] or self.controls['doorRightOpen']) and not self.atStation:
        #     self.atStation = True  # Set variable to indicate the train is at a station

            # Randomly generate the number of passengers leaving the train
            if self.passCount > 0:
                passengers_depart = random.randint(0, self.passCount)  # Random number of departing passengers
                self.passengers -= passengers_depart

            # Pick up passengers through track model
            max_pickup = self.maxOccupancy - self.passengers  # Calculate maximum possible entries
            passenger_enter = random.randint(0, trans_max)  # Random number of passengers entering
            #passengers_board = self.block.get_passengers(random_pass_entry)  # Assuming this method is defined
            self.passCount += passenger enter

            # Calculate new mass based on passenger count
            self.trainMass = (self.numberOfCars * 40900) + (self.passCount * 150)  # Weight of passengers in pounds
        #leaving the station
        elif not self.controls['doorLeftOpen'] and not self.controls['doorRightOpen']:
            self.atStation = False  # Reset boolean when the doors are closed