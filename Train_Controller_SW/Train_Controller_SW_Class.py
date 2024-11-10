import sys
import time
import requests

URL = 'http://127.0.0.1:5000'


############################
#  Variable Declaration 
############################

#Bools
class Train_Controller:

    #train constructor function
    def __init__ (self, id):
        self.manual_mode = False
        self.e_brake = False
        self.s_brake = False
        self.r_door = False
        self.l_door = False
        self.i_light = False
        self.o_light = False
        self.failure_engine = False
        self.failure_brake = False
        self.failure_signal = False
        self.station_reached = False

        #Floats
        self.k_p = 0.0
        self.k_i = 0.0
        self.time_world = 0.0
        self.commanded_power = 0.0
        self.ek = 0.0
        self.ek_1 = 0.0
        self.T = 0.09 #time samples of 50 ms
        self.uk = 0.0
        self.uk_1 = 0.0

        #Ints
        self.authority = 0
        self.actual_velocity = 0
        self.commanded_velocity = 0
        self.setpoint_velocity = 0
        self.temperature = 70
        self.beacon_info = 0
        self.train_id = id

        #Strings
        self.pa_announcement = ""

        #output dictionaries
        self.commanded_power_dict = {
            "commanded_power": self.commanded_power,
            "train_id": self.train_id
        }

        self.pa_announcement_dict = {
            "pa_announcement": self.pa_announcement,
            "train_id": self.train_id
        }

        self.temperature_dict = {
            "temperature": self.temperature,
            "train_id": self.train_id
        }

        self.lights_dict = {
            "o_light": self.o_light,
            "i_light": self.i_light,
            "train_id": self.train_id
        }

        self.doors_dict = {
            "l_door": self.l_door,
            "r_door": self.r_door,
            "train_id": self.train_id
        }

        self.brakes_dict = {
            "s_brake": self.s_brake,
            "e_brake": self.e_brake,
            "train_id": self.train_id
        }


    ############################
    #  Function Declaration 
    ############################



    ############################
    #  Set Functions 
    ############################

    #set manual mode
    def set_manual_mode(self, truth):
        self.manual_mode = truth

    #set doors
    def set_l_door(self, left):
        self.l_door = left
        self.doors_dict["l_door"] = self.l_door

    def set_r_door(self, right):
        self.r_door = right
        self.doors_dict["r_door"] = self.r_door

    #set lights
    def set_i_light(self, inside):
        self.i_light = inside
        self.lights_dict["i_light"] = self.i_light

    #set lights
    def set_o_light(self, outside):
        self.o_light = outside
        self.lights_dict["o_light"] = self.o_light

    #set lights
    def set_beacon_info(self, info):
        self.beacon_info = info
        self.decode_signal()

    #set station_reached
    def set_station_reached(self, reached):
        self.station_reached = reached

    #set temperature
    def set_temperature(self, temp):
        self.temperature = temp
        self.temperature_dict["temperature"] = self.temperature
        
    #set brakes
    def set_s_brake(self, status):
        self.s_brake = status
        self.brakes_dict["s_brake"] = self.s_brake

    def set_e_brake(self, status):
        self.e_brake = status
        self.brakes_dict["e_brake"] = self.e_brake

    #set authority
    def set_authority(self, distance):
        self.authority = distance

    #set velocities
    def set_actual_velocity(self, v):
        self.actual_velocity = v

    def set_commanded_velocity(self, v):
        self.commanded_velocity = v

    def set_setpoint_velocity(self, v):
        self.setpoint_velocity = v

    #Engineer's constants
    def set_k_p(self, k):
        self.k_p = k

    def set_k_i(self, k):
        self.k_i = k

    #set commanded power
    def set_commanded_power(self, power):
        self.commanded_power = power

        self.commanded_power_dict["commanded_power"] = self.commanded_power

    #set failure modes
    def set_failure_engine(self, truth):
        self.failure_engine = truth

    def set_failure_brake(self, truth):
        self.failure_brake = truth

    def set_failure_signal(self, truth):
        self.failure_signal = truth

    def set_train_id(self, number):
        self.train_id = number

    def get_train_id(self):
        return self.train_id


    ############################
    #  Get Functions 
    ############################

    #get manual mode
    def get_manual_mode(self):
        return self.manual_mode

    #get door status
    def get_l_door(self):
        return self.l_door

    def get_r_door(self):
        return self.r_door

    #get light status
    def get_i_light(self):
        return self.i_light

    def get_o_light(self):
        return self.o_light
    
    #get temnperature
    def get_temperature(self):
        return self.temperature

    #get brakes
    def get_s_brake(self):
        return self.s_brake

    def get_e_brake(self):
        return self.e_brake
    
    #get authority
    def get_authority(self):
        return self.authority

    #set velocities
    def get_actual_velocity(self):
        return self.actual_velocity

    def get_commanded_velocity(self):
        return self.commanded_velocity

    def get_setpoint_velocity(self):
        return self.setpoint_velocity

    #get failure modes
    def get_failure_engine(self):
        return self.failure_engine

    def get_failure_brake(self):
        return self.failure_brake

    def get_failure_signal(self):
        return self.failure_signal
    
    #checks if any failures exist
    def check_any_failures(self):
        if self.failure_engine or self.failure_brake or self.failure_signal:
            return True
        else:
            return False
    
    #set commanded power
    def get_commanded_power(self):
        return self.commanded_power
    
    #pa announcement string
    def get_pa_announcement(self):
        return self.pa_announcement
    
    def get_station_reached(self):
        return self.station_reached
    

    #checks if authority is at distance where braking should occur in auto mode
    def stop_at_station(self):

        #checks if authorirt is less than Vi^2 / 2*max-braking
        if self.authority <= self.actual_velocity**2 / 2.4:
            self.s_brake = True
            return True
        else:
            self.s_brake = False
            return False
        
    #this function updates authority in real time in order to have an accurate reading for the driver
    def update_authority(self):
        self.authority -= self.actual_velocity*self.T   #multiple time interval by actual velocity



    


    #this function will return the setpoint velocity based on the commaned velocity and user inputed set point velocity
    #if the user inputs a value higher than commaned velocity, the set point will default to the commanded velocity
    def SetSetPointVelocity(self):
        if float(self.setpoint_velocity) > float(self.commanded_velocity):
            self.setpoint_velocity = self.commanded_velocity

    #this function will decode the beacon signal
    def decode_signal(self):

        #Check if beacon is an enter station beacon
        self.station_reached = True

        if self.beacon_info == "1":
            self.pa_announcement = "Lebron"
        elif self.beacon_info == "2":
            self.pa_announcement = "Now Arriving at Station B"
        elif self.beacon_info == "3":
            self.pa_announcement = "Now Arriving at Station C"
        else:
            self.pa_announcement = ""

        self.pa_announcement_dict["pa_announcement"] = self.pa_announcement

    #this function will return the commanded Power and will be called every 50 ms
    def calculate_commanded_power(self):

        #check setpoint speed first or if any brakes are being pressed
        if self.setpoint_velocity <= self.actual_velocity or self.s_brake or self.e_brake:
            self.commanded_power = 0
            self.ek = 0
            self.ek_1 = 0
            self.uk = 0
            self.uk_1 = 0
            return
        
        #update ek_1 and uk_1
        self.ek_1 = self.ek
        self.uk_1 = self.uk

        #calculate current ek (setpoint velocity - actual velocity)
        self.ek = self.setpoint_velocity - self.actual_velocity

        #calculate uk
        if self.commanded_power < 120000:   #commanded vs maximum power
            self.uk = self.uk_1 + self.T/2*(self.ek + self.ek_1)     
        else:
            self.uk = self.uk_1

        #calculate commaneded power (kp*ek + ki*uk)
        self.set_commanded_power(self.k_p*self.ek + self.k_i*self.uk)

        response = requests.post(URL + "/train-model/recieve-commanded-power", json=self.commanded_power_dict)





    # Initialize the counter at the current time (in seconds)
    start_time = time.time()

    # To get the number of seconds that have passed since the start
    #def get_seconds_since_start():
        #return int(time.time() - start_time)

