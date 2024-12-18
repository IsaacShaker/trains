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
    start_temperature_adjustment_signal = pyqtSignal(float)

    def __init__(self, tc_list):
        super().__init__()
        self.adjust_timer = QTimer(self)
        self.adjust_timer.timeout.connect(self.update_temperature)

        self.start_temperature_adjustment_signal.connect(self.start_adjusting_temperature)

        # Initialize variables

        #For the dynamic list
        self.train_controller_list = tc_list

        #Train number
        self.ID=0

        #Key outputs
        self.currentVelocity = 0.0
        self.currAccel = 0.0

        self.commandedSpeed = 0.0
        self.authority = 0.0
        self.beaconInfo=0
        self.grade=0.0

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
        self.station_passengers=0
        self.passengers_leaving=0

        #Failure Mode
        self.signalPickupFailure = False
        self.engineFailure = False
        self.brakeFailure = False

        self.stationName = ""

        #Calculations
        self.currForce = 0.0
        self.currPower = 0.0
        self.samplePeriod = 0.09 
        self.mitch_var=1
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

        self.passenger_dict = {
            "train_id" : self.ID,
            "passengers_leaving": self.passengers_leaving
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
        #print(f"Headlights set to {'on' if state else 'off'}.")
        self.ui_refresh.emit()

    def set_insideLights(self, state: bool):
        self.insideLights = state
       # print(f"Inside lights set to {'on' if state else 'off'}.")
        self.ui_refresh.emit()

    def set_announcements(self, message: str):
        self.announcements = message
        #print(f"Announcement set to: {message}")
        self.ui_refresh.emit()

    def set_rightDoor(self, state: bool):
        self.rightDoor = state
       # print(f"Right door set to {'open' if state else 'closed'}.")
        self.ui_refresh.emit()

    def set_leftDoor(self, state: bool):
        self.leftDoor = state
        #print(f"Left door set to {'open' if state else 'closed'}.")
        self.ui_refresh.emit()

    def set_commandedTemperature(self, temp: float):
        self.commandedTemperature = temp
        #print(f"Commanded temperature set to {temp}°F.")
        self.start_temperature_adjustment_signal.emit(temp)
        self.ui_refresh.emit()

    def set_commandedSpeed(self, speed: float):
        self.commandedSpeed = self.kmh_to_ms(speed)
        self.commanded_velocity_dict["train_id"]=self.ID
        self.commanded_velocity_dict["commanded_velocity"]=self.commandedSpeed
        #print(f"Commanded speed set to {speed} km/hr.")
        response = requests.post(URL + "/train-controller/receive-commanded-velocity", json=self.commanded_velocity_dict)
        self.ui_refresh.emit()

    def set_authority(self, authority: float):
        
        self.authority = authority
        self.authority_dict["train_id"]=self.ID
        self.authority_dict["authority"]=self.authority
        #print(f"Authority set to {authority}.")
        if(authority is not None):
            response = requests.post(URL + "/train-controller/receive-authority", json=self.authority_dict)
        self.ui_refresh.emit()

    def set_beaconInfo(self, info: string):
        self.beaconInfo = info
        self.beacon_info_dict["train_id"]=self.ID
        self.beacon_info_dict["beacon_info"]=self.beaconInfo
        #print(f"Beacon info set to {info}.")
        response = requests.post(URL + "/train-controller/receive-beacon-info", json=self.beacon_info_dict)
        self.ui_refresh.emit()

    def set_grade(self, grade: float):
        self.grade=grade

    def set_currentVelocity(self, vel: float):
        self.currentVelocity=vel
        self.actual_velocity_dict["train_id"]=self.ID
        self.actual_velocity_dict["actual_velocity"]=self.currentVelocity
        # response = requests.post(URL + "/train-controller/receive-actual-velocity", json=self.actual_velocity_dict)
        if self.ID != 0:
            self.train_controller_list[self.ID-1].set_actual_velocity(self.currentVelocity)
        #response = requests.post(URL + "/track-model/get-data/current-speed", json=self.actual_velocity_dict)
        self.ui_refresh.emit()

    def set_signal_pickup_failure(self, state: bool):
        self.signalPickupFailure=state
        self.failure_modes_dict["train_id"]=self.ID
        self.failure_modes_dict["failure_signal"]=self.signalPickupFailure
        response = requests.post(URL + "/train-controller/receive-failure-modes", json=self.failure_modes_dict)
        self.ui_refresh.emit()

    def set_engine_failure(self, state: bool):
        self.engineFailure=state
        self.failure_modes_dict["train_id"]=self.ID
        self.failure_modes_dict["failure_engine"]=self.engineFailure
        response = requests.post(URL + "/train-controller/receive-failure-modes", json=self.failure_modes_dict)
        self.ui_refresh.emit()

    def set_brake_failure(self, state: bool):
        self.brakeFailure=state
        self.failure_modes_dict["train_id"]=self.ID
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
        #print(f"Power set to {cmd}.")
        self.receive_power()
        self.ui_refresh.emit()

    def set_samplePeriod(self, input):
        if(self.ID == 0):
            self.samplePeriod = 0.09 * input
        else:
            self.samplePeriod = 0.09

    #Determine the random amout of passengers leaving
    def set_passengers_leaving(self):
        if self.passCount > 0:
            self.passengers_leaving = random.randint(0, self.passCount)
        self.passenger_dict["train_id"]=self.ID
        print(f"ID:{self.ID}")
        self.passenger_dict["passengers_leaving"]=self.passengers_leaving
        print(f"Pass leaving: {self.passengers_leaving}")
        #API CALL
        response = requests.post(URL + "/track-model/receive-leaving-passengers", json=self.passenger_dict)
        #Nate call self.update_passengers()

    def set_station_passengers(self, num: int):
        self.station_passengers=num
        self.update_passengers()

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

    #Meters per second to miles per hour
    def mps_to_mph(self, vel):
        vel=vel*2.2369
        return vel

    #Miles per hour to meters per second
    def mph_to_mps(self, vel):
        vel=vel/2.2369
        return vel

    #Meters to feet
    def m_to_ft(self, num):
        num=num*3.2808
        return num

    #Tons to kilograms
    def tons_to_kg(self, mass):
        mass=mass*1000
        return mass

    #kilometers to hour to meters per second
    def kmh_to_ms(self,speed):
        speed=(((speed*1000)/60)/60)
        return speed
    
    #Tons to newtons
    def tons_to_N(self,mass):
        mass=mass*1000*9.80665
        return mass

    def start_adjusting_temperature(self):
        self.adjust_timer.start(100)  # Update every 100 ms

    #First order differential for temp
    def update_temperature(self):
        if abs(self.temperature - self.commandedTemperature) > 0.01:
            # First-order differential equation update
            self.temperature += 0.1 * (self.commandedTemperature - self.temperature)
            #print(f"Current Temperature: {self.temperature:.2f}°C")
            # Update the temperature label in the UI
            self.temperature_changed.emit(self.temperature)
        else:
            #print("Target temperature reached.")
            self.adjust_timer.stop()  # Stop the timer when the target is reached

    def calc_total_mass(self):    
        # Convert train weight to pounds
        car_weight_pounds = self.CAR_MASS * 2204.623
        train_weight_pounds=car_weight_pounds*self.numberOfCars        
        # Calculate total weight of crew and passengers
        total_people_weight = (self.crewCount + self.passCount) * self.PERSON_WEIGHT_POUNDS        
        # Total weight in pounds
        total_weight_pounds = train_weight_pounds + total_people_weight        
        # Convert total weight to tons
        total_weight_tons = total_weight_pounds / 2204.623
        #print (total_weight_tons)
        self.totalMass=total_weight_tons        
        #return total_weight_tons

    def calc_total_length(self):
        if(self.numberOfCars<5):
            self.trainLength=32.2-((5-self.numberOfCars)*6.6)
        #print(f"Length: {self.trainLength}")

    #Ensures force does not exceed max or is not undefined
    def force_limiter(self):
        max_force = self.tons_to_kg(self.totalMass) * 0.5
        #If our force passes the max allowed
        if self.currForce > max_force:
            self.currForce = max_force
        #If the power is at 0 and we are not moving or the emergency brake is pulled
        elif (self.currPower == 0 and self.lastVel == 0) or self.emergencyBrake or self.engineFailure:
            self.currForce = 0
        #If the train is not moving, add limiter so the force is not infinite
        elif self.lastVel == 0:
            self.currForce = max_force

    #Ensures acceleration is not too high and brakes/failure modes affect it
    def acceleration_limiter(self):
        if (self.currAccel > self.ACCELERATION_LIMIT and not self.serviceBrake and not self.emergencyBrake):
            # If all brakes are OFF and self.currAccel is above the limit
            self.currAccel = self.ACCELERATION_LIMIT
        elif (self.serviceBrake and not self.emergencyBrake and not self.brakeFailure): # self.currAccel < self.DECELERATION_LIMIT_SERVICE and
            # If the service brake is ON and self.currAccel is below the limit
            if(self.currentVelocity !=0):
                self.currAccel = self.S_BRAKE_ACC
            else:
                self.currAccel = 0
        elif (self.emergencyBrake): # self.currAccel < self.DECELERATION_LIMIT_EMERGENCY and
            # If the emergency brake is ON and self.currAccel is below the limit
            if(self.currentVelocity !=0):
                self.currAccel = self.E_BRAKE_ACC
            else:
                self.currAccel = 0

    #Set new amount of passengers and update the passenger count
    def update_passengers(self):
        # Maximum passengers to enter
        max_new_passengers = self.MAX_PASSENGERS - self.passCount  
        # Random number of passengers entering from the amount at the station
        if(self.station_passengers>max_new_passengers):
            self.station_passengers=max_new_passengers
        #Update our passenger count
        self.passCount += self.station_passengers

        # Calculate new mass based on passenger count
        self.calc_total_mass()

        #Update the passenger and weight information in the UI
        self.passengers_changed.emit()

    #When power command is received, use Newton's Laws and the train control equations
    def receive_power(self):
        if(self.engineFailure):
            self.currPower = 0
        previousAcceleration=self.currAccel
        # Check to avoid division by zero in case velocity is zero
        if self.currentVelocity != 0:
            self.currForce = self.currPower / self.currentVelocity
        else:
             #Force to 0 if velocity is 0 to avoid divide by zero error
            self.currForce = 0
        #print(self.currForce)
        self.force_limiter()
       # print(self.currForce)

        #Acceleration calculations
        if self.totalMass != 0:
            self.currAccel = self.currForce / (self.tons_to_kg(self.totalMass)) 
        # Ensure totalMass is not zero
        else:
            self.currAccel = 0
        #print(self.currAccel)
        self.acceleration_limiter()
        #print(self.currAccel)

        #Velocity calculations
        velocityNew = self.currentVelocity + (((self.samplePeriod / 2)/self.mitch_var) * (self.currAccel + previousAcceleration))
        if(velocityNew >= self.VELOCITY_LIMIT):
            # If the velocity is greater than max speed
            velocityNew = self.VELOCITY_LIMIT # m/s
        if(velocityNew <= 0):
            # If the velocity is negative
            velocityNew = 0

        #Set and send velocity
        self.set_currentVelocity(velocityNew)

        self.lastVel=self.currentVelocity

