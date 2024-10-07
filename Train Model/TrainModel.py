# TrainModel.py

import time
import random

class TrainModel:
    def __init__(self):

        # Initialize variables
        self.commandedSpeed = 0.0
        self.currentVelocity = 0.0
        self.currAccel = 0.0
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
        self.totalMass = 0
        self.numberOfCars = 5
        self.crewCount = 2
        self.passCount = 0
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False
        self.atStation = False
        self.currForce = 0
        self.currPower = 0

        self.MAX_PASSENGERS=222
        self.PERSON_WEIGHT_POUNDS=150
        self.CAR_MASS = 40.9
        self.E_BRAKE_ACC = 2.73
        self.S_BRAKE_ACC = 1.2
        self.ACCELERATION_LIMIT=0.5

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
    
    def mps_to_mph(self, vel):
        vel=vel*2.2369
        return vel

    def ms2_to_fts2(self, num):
        num=num*3.2808
        return num

    def adjust_temperature(self, target_temperature):
        while abs(self.temperature - target_temperature) > 0.1:
            # First-order differential equation update
            self.temperature += .1 * (target_temperature - self.temperature)

            # Simulate time passage (you can adjust the sleep duration)
            time.sleep(0.1)  # Sleep for 100ms for a smoother transition
            print(f"Current Temperature: {self.temperature:.2f}°C")

        print("Target temperature reached.")

    def calc_total_mass(self):
    
        # Convert train weight to pounds
        car_weight_pounds = self.CAR_MASS * 2000

        train_weight_pounds=car_weight_pounds*self.numberOfCars
        
        # Calculate total weight of crew and passengers
        total_people_weight = (self.crewCount + self.passCount) * self.PERSON_WEIGHT_POUNDS
        
        # Total weight in pounds
        total_weight_pounds = train_weight_pounds + total_people_weight
        
        # Convert total weight to tons
        total_weight_tons = total_weight_pounds / 2000  # Convert back to tons

        print (total_weight_tons)

        totalMass=total_weight_tons
        
        return total_weight_tons

    def calc_total_length(self):
        if(numberOfCars<5):
            trainLength=32.2-((5-numberOfCars)*6.6)

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
        if (accelerationCalc > self.ACCELERATION_LIMIT and not serviceBrake and not emergencyBrake):
            # If all brakes are OFF and accelerationCalc is above the limit
            accelerationCalc = self.ACCELERATION_LIMIT
        elif (serviceBrake and not emergencyBrake): # accelerationCalc < self.DECELERATION_LIMIT_SERVICE and
            # If the service brake is ON and accelerationCalc is below the limit
            accelerationCalc = self.DECELERATION_LIMIT_SERVICE
        elif (not serviceBrake and emergencyBrake): # accelerationCalc < self.DECELERATION_LIMIT_EMERGENCY and
            # If the emergency brake is ON and accelerationCalc is below the limit
            accelerationCalc = self.DECELERATION_LIMIT_EMERGENCY
        elif (serviceBrake and emergencyBrake): # Edge case if both emergency brake and service brake are turned on
            accelerationCalc = self.DECELERATION_LIMIT_EMERGENCY # Emergency brake takes priority

    def update_passengers(self):
        # If the doors are open and the train was not at a station in the previous loop
        if (not self.leftDoor or not self.rightDoor) and not self.atStation:
            self.atStation = True  # Set variable to indicate the train is at a station
            print(f"Current Passengers: {self.passCount}")
            # Randomly generate the number of passengers leaving the train
            if self.passCount > 0:
                passengers_depart = random.randint(0, self.passCount)  # Random number of departing passengers
                self.passCount -= passengers_depart
            print(f"Passengers after departure: {self.passCount}")
            # Pick up passengers through track model
            max_pickup = self.MAX_PASSENGERS - self.passCount  # Calculate maximum possible entries
            passengers_enter = random.randint(0, max_pickup)  # Random number of passengers entering
            #passengers_board = self.block.get_passengers(random_pass_entry)  # Assuming this method is defined
            self.passCount += passengers_enter
            print(f"Passengers after board: {self.passCount}")
            # Calculate new mass based on passenger count
            self.calc_total_mass()

        #leaving the station
        elif not self.leftDoor and not self.rightDoor:
            self.atStation = False  # Reset boolean when the doors are closed

    def train_model_receive_power(self):
        if(self.engineFailure):
            currPower = 0

        # FORCE
        currForce = (currPower/currentVelocity)
        limit_force()

        # ACCELERATION
        currAccel = (currForce/totalMass) # Acceleration Limit: 0.5 m/s^2     Deceleration Limit(service brake): 1.2 m/s^2    Deceleration Limit(emergency brake): 2.73 m/s^2
        limit_accel()


        # VELOCITY
        velocityCalc = currentSpeed + ( (samplePeriod / 2) * (accelerationCalc + previousAcceleration) ) # Velocity Limit: 19.4444 m/s
        logger.debug("velocityCalc in MPH = %f", velocityCalc * Converters.mps_to_MPH)
        if(velocityCalc >= self.VELOCITY_LIMIT):
            # If the velocity is GREATER than max train speed
            velocityCalc = self.VELOCITY_LIMIT # m/s
        #if(velocityCalc >= speedLimitBlock):
            # If the velocity is GREATER than the block's speed limit
        #    velocityCalc = speedLimitBlock
        #    logger.debug("speedLimitBlock = %f", speedLimitBlock)
        if(velocityCalc <= 0):
            # If the velocity is LESS than 0
            velocityCalc = 0

        currentPosition = 0
        positionCalc = 0

        
        # POSITION
        positionCalc = (velocityCalc*samplePeriod)
        currentPosition = previousPosition + positionCalc

        # Set all the parameters in the train object
        self.m_trainList[trainId].m_power = powerStatus
        self.m_trainList[trainId].m_currentSpeed = velocityCalc * Converters.mps_to_MPH
        self.m_trainList[trainId].m_acceleration = accelerationCalc
