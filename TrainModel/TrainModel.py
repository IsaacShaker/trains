# TrainModel.py

import time
import random
import requests
import string

URL = 'http://127.0.0.1:5000'

from PyQt6.QtCore import pyqtSignal, QObject, QTimer

class TrainModel(QObject):

    temperature_changed = pyqtSignal(float)
    power_changed = pyqtSignal()
    passengers_changed = pyqtSignal()
    ui_refresh = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.adjust_timer = QTimer()
        self.adjust_timer.timeout.connect(self.update_temperature)

        # Initialize variables

        #Train number
        self.ID=0

        #Key outputs
        self.currentVelocity = 0.0
        self.currAccel = 0.0

        self.commandedSpeed = 0.0
        self.authority = 0.0
        self.beaconInfo=0

        #Brakes
        self.emergencyBrake = False
        self.serviceBrake = False

        #User mode other outputs
        self.headLights = False
        self.insideLights = False
        self.announcements = ""
        self.rightDoor = False
        self.leftDoor = False
        self.temperature = 68.0 #F
        self.commandedTemperature = 0

        #Dimensions
        self.trainLength = 32.2 #m
        self.trainWidth = 2.65 #m
        self.trainHeight = 3.42 #m
        self.totalMass = 204.65 #tons
        self.numberOfCars = 5
        self.crewCount = 2
        self.passCount = 0

        #Failure Mode
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        self.stationName = ""

        #Calculations
        self.currForce = 0.0
        self.currPower = 0.0
        self.samplePeriod = 0.05
        self.lastVel=0.0

        #Constants
        self.MAX_PASSENGERS=222
        self.PERSON_WEIGHT_POUNDS=150 #pounds
        self.CAR_MASS = 40.9 #tons
        self.E_BRAKE_ACC = -2.73 #m/s^2
        self.S_BRAKE_ACC = -1.2 #m/s^2
        self.ACCELERATION_LIMIT=0.5 #m/s^2
        self.VELOCITY_LIMIT=19.4444444 #m/s

    #Dictionaries
    #input dictionary
        self.authority_dict = {
            "train_id" : self.ID,
            "authority": self.authority
        }

        self.commanded_velocity_dict = {
            "train_id" : self.ID,
            "commanded_velocity": self.commandedSpeed
        }

        self.beacon_info_dict = {
            "train_id" : self.ID,
            "beacon_info": self.beaconInfo
        }

        self.actual_velocity_dict = {
            "train_id" : self.ID,
            "actual_velocity": self.currentVelocity
        }

        self.failure_modes_dict = {
            "train_id" : self.ID,
            "failure_engine": self.engineFailure,
            "failure_brake": self.brakeFailure,
            "failure_signal": self.signalPickupFailure
        }

        # self.brakes_dict = {
        #     "train_id" : self.ID,
        #     "e_brake" : self.emergencyBrake,
        #     "s_brake" : self.serviceBrake
        # }

    #Setters and getters for api

    #Setters
    def set_headLights(self, state: bool):
        self.headLights = state
        print(f"Headlights set to {'on' if state else 'off'}.")
        self.ui_refresh.emit()

    def set_insideLights(self, state: bool):
        self.insideLights = state
        print(f"Inside lights set to {'on' if state else 'off'}.")
        self.ui_refresh.emit()

    def set_announcements(self, message: str):
        self.announcements = message
        print(f"Announcement set to: {message}")
        self.ui_refresh.emit()

    def set_rightDoor(self, state: bool):
        self.rightDoor = state
        print(f"Right door set to {'open' if state else 'closed'}.")
        self.ui_refresh.emit()

    def set_leftDoor(self, state: bool):
        self.leftDoor = state
        print(f"Left door set to {'open' if state else 'closed'}.")
        self.ui_refresh.emit()

    def set_commandedTemperature(self, temp: float):
        self.commandedTemperature = temp
        self.start_adjusting_temperature()
        print(f"Commanded temperature set to {temp}°F.")
        self.ui_refresh.emit()

    def set_commandedSpeed(self, speed: float):
        self.commandedSpeed = self.mph_to_mps(speed)
        self.commanded_velocity_dict["commanded_velocity"]=self.commandedSpeed
        print(f"Commanded speed set to {speed} m/s.")
        response = requests.post(URL + "/train-controller/receive-commanded-velocity", json=self.commanded_velocity_dict)
        self.ui_refresh.emit()

    def set_authority(self, authority: float):
        self.authority = authority
        self.authority_dict["authority"]=self.authority
        print(f"Authority set to {authority}.")
        response = requests.post(URL + "/train-controller/receive-authority", json=self.authority_dict)
        self.ui_refresh.emit()

    def set_beaconInfo(self, info: string):
        self.beaconInfo = info
        self.beacon_info_dict["beacon_info"]=self.beaconInfo
        print(f"Beacon info set to {info}.")
        response = requests.post(URL + "/train-controller/receive-beacon-info", json=self.beacon_info_dict)
        self.ui_refresh.emit()

    def set_currentVelocity(self, vel: float):
        self.currentVelocity=vel
        self.actual_velocity_dict["actual_velocity"]=self.currentVelocity
        response = requests.post(URL + "/train-controller/receive-actual-velocity", json=self.actual_velocity_dict)
        self.ui_refresh.emit()

    def set_signal_pickup_failure(self, state: bool):
        self.signalPickupFailure=state
        self.failure_modes_dict["failure_signal"]=self.signalPickupFailure
        response = requests.post(URL + "/train-controller/receive-failure-modes", json=self.failure_modes_dict)
        self.ui_refresh.emit()

    def set_engine_failure(self, state: bool):
        self.engineFailure=state
        self.failure_modes_dict["failure_engine"]=self.engineFailure
        response = requests.post(URL + "/train-controller/receive-failure-modes", json=self.failure_modes_dict)
        self.ui_refresh.emit()

    def set_brake_failure(self, state: bool):
        self.brakeFailure=state
        self.failure_modes_dict["failure_brake"]=self.brakeFailure
        response = requests.post(URL + "/train-controller/receive-failure-modes", json=self.failure_modes_dict)
        self.ui_refresh.emit()

    def set_serviceBrake(self, state:bool):
        self.serviceBrake = state


    def set_emergencyBrake(self, state: bool):
        self.emergencyBrake = state
        self.ui_refresh.emit()

    def set_commanded_power(self, cmd: float):
        self.currPower=cmd
        print(f"Power set to {cmd}.")
        self.receive_power()
        self.ui_refresh.emit()

    #Getters
    def get_commandedSpeed(self):
        return self.commandedSpeed

    # Getter for authority
    def get_authority(self):
        return self.authority

    # Getter for beaconInfo
    def get_beaconInfo(self):
        return self.beaconInfo

    # Getter for currentVelocity
    def get_currentVelocity(self):
        return self.currentVelocity

    def mps_to_mph(self, vel):
        vel=vel*2.2369
        return vel

    def mph_to_mps(self, vel):
        vel=vel/2.2369
        return vel

    def m_to_ft(self, num):
        num=num*3.2808
        return num

    def tons_to_kg(self, mass):
        mass=mass*907.18474
        return mass

    def start_adjusting_temperature(self):
        self.adjust_timer.start(100)  # Update every 100 ms

    def update_temperature(self):
        if abs(self.temperature - self.commandedTemperature) > 0.01:
            # First-order differential equation update
            self.temperature += 0.1 * (self.commandedTemperature - self.temperature)
            print(f"Current Temperature: {self.temperature:.2f}°C")
            # Update the temperature label in the UI
            self.temperature_changed.emit(self.temperature)
        else:
            print("Target temperature reached.")
            self.adjust_timer.stop()  # Stop the timer when the target is reached

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

        self.totalMass=total_weight_tons
        
        #return total_weight_tons

    def calc_total_length(self):
        if(self.numberOfCars<5):
            self.trainLength=32.2-((5-self.numberOfCars)*6.6)
        print(f"Length: {self.trainLength}")

    def limit_force(self):
        max_force = self.tons_to_kg(self.totalMass) * 0.5
        #If our force passes the max allowed
        if self.currForce > max_force:
            self.currForce = max_force
        #If the power is at 0 and we are not moving or the emergency brake is pulled
        elif (self.currPower == 0 and self.lastVel == 0) or self.emergencyBrake or self.signalPickupFailure or self.engineFailure or self.brakeFailure:
            self.currForce = 0
        #If the train is not moving, add limiter so the force is not infinite
        elif self.lastVel == 0:
            self.currForce = max_force

    def limit_accel(self):
        failure_mode_active= self.signalPickupFailure or self.engineFailure or self.signalPickupFailure
        if (self.currAccel > self.ACCELERATION_LIMIT and not self.serviceBrake and not self.emergencyBrake):
            print("Case 1")
            # If all brakes are OFF and self.currAccel is above the limit
            self.currAccel = self.ACCELERATION_LIMIT
        elif (self.serviceBrake and not self.emergencyBrake and not failure_mode_active): # self.currAccel < self.DECELERATION_LIMIT_SERVICE and
            print("Case 2")
            # If the service brake is ON and self.currAccel is below the limit
            self.currAccel = self.S_BRAKE_ACC
        elif (not self.serviceBrake and (self.emergencyBrake or failure_mode_active)): # self.currAccel < self.DECELERATION_LIMIT_EMERGENCY and
            # If the emergency brake is ON and self.currAccel is below the limit
            print("IN THERE")
            if(self.currentVelocity !=0):
                self.currAccel = self.E_BRAKE_ACC
            else:
                self.currAccel = 0
        elif (self.serviceBrake and (self.emergencyBrake or failure_mode_active)): # Edge case if both emergency brake and service brake are turned on
            print("Case 4")
            if(self.currentVelocity !=0):
                self.currAccel = self.E_BRAKE_ACC
            else:
                self.currAccel = 0
        #print(f"Current Acceleration: {self.currAccel}")

    def update_passengers(self):
        # If the doors are open and the train was not at a station in the previous loop
        #if (not self.leftDoor or not self.rightDoor) and not self.atStation:
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

            self.passengers_changed.emit()

        #leaving the station
        #elif not self.leftDoor and not self.rightDoor:
            #self.atStation = False  # Reset boolean when the doors are closed

    def receive_power(self):
        if(self.engineFailure):
            self.currPower = 0

        previousAcceleration=self.currAccel

        # Check to avoid division by zero in case velocity is zero
        if self.currentVelocity != 0:
            self.currForce = self.currPower / self.currentVelocity
        else:
            self.currForce = 0  # Set force to zero if velocity is zero
        #print(f"Force: {self.currForce}")
        self.limit_force()

        #print(f"Force: {self.currForce}")

            # ACCELERATION
        if self.totalMass != 0:
            self.currAccel = self.currForce / (self.tons_to_kg(self.totalMass))  # Ensure totalMass is not zero
        else:
            self.currAccel = 0

        self.limit_accel()

        #print(f"Acceleration: {self.currAccel}")

        # VELOCITY
        velocityNew = self.currentVelocity + ( (self.samplePeriod / 2) * (self.currAccel + previousAcceleration) ) # Velocity Limit: 19.4444 m/s
        if(velocityNew >= self.VELOCITY_LIMIT):
            # If the velocity is GREATER than max train speed
            velocityNew = self.VELOCITY_LIMIT # m/s
        if(velocityNew <= 0):
            # If the velocity is LESS than 0
            velocityNew = 0

        self.set_currentVelocity(velocityNew)

        #print(f"Velocity: {self.currentVelocity}")

        
        self.power_changed.emit()

        self.lastVel=self.currentVelocity
        # currentPosition = 0
        # positionCalc = 0

        
        # POSITION
        # positionCalc = self.currentVelocity*self.samplePeriod
        # currentPosition = previousPosition + positionCalc
