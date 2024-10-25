import sys
import time
############################
#  Variable Declaration 
############################

#Bools
class Train_Controller:

    #train constructor function
    def __init__ (self):
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

        #Strings
        self.pa_announcement = ""

    ############################
    #  Function Declaration 
    ############################



    ############################
    #  Set Functions 
    ############################

    #set doors
    def set_doors(self, left, right):
        self.l_door = left
        self.r_door = right

    #set lights
    def set_lights(self, inside, outside):
        self.i_light = inside
        self.o_light = outside

    #set lights
    def set_beacon_info(self, info):
        self.beacon_info = info
        self.decode_signal()

    #set station_reached
    def set_station_reached(self, reached):
        self.station_reached = reached




    ############################
    #  Get Functions 
    ############################
    
    #pa announcement string
    def get_pa_announcement(self):
        return self.pa_announcement
    
    def get_station_reached(self):
        return self.station_reached

    


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

    #this function will return the commanded Power and will be called every 50 ms
    def Set_Commanded_Power(self):

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
        self.commanded_power = self.k_p*self.ek + self.k_i*self.uk

    # Initialize the counter at the current time (in seconds)
    start_time = time.time()

    # To get the number of seconds that have passed since the start
    #def get_seconds_since_start():
        #return int(time.time() - start_time)

