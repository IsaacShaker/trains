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
        self.failure_brakes = False
        self.failure_signal = False

        #Floats
        self.k_p = 0.0
        self.k_i = 0.0
        self.power = 0.0
        self.time_world = 0.0

        #Ints
        self.authority = 0
        self.actual_velocity = 0
        self.commanded_velocity = 0
        self.setpoint_velocity = 0
        self.temperature = 70
        self.beacon_info = 0
        self.train_count = 0 #won't use this number much into we implement other modules

    ############################
    #  Function Declaration 
    ############################

    #this function will calculate the velocity
    def SetActualVelocity():
        v = 5 #############NOT DONE################
        return v

    #this function will return the setpoint velocity based on the commaned velocity and user inputed set point velocity
    #if the user inputs a value higher than commaned velocity, the set point will default to the commanded velocity
    def SetSetPointVelocity(user_setpoint_v, commanded_v):
        if user_setpoint_v > commanded_v:
            return commanded_v
        else:
            return user_setpoint_v


    #this function will be for automode to set the lights on or off (WILL HAVE TO ADJUST FOR TUNNELS)
    def SetLights(time):
        if time >= 20.00 or time < 8.00:       #Between 8 pm and 8 am, lights will be on
            return True
        else:
            return False                        #lights will be off at other times

    #this function will return true if a failure mode has occured and the E-brake has be pulled. Otherwise it will return false
    def FailureModes(failure_e, failure_b, failure_s):
        if failure_e or failure_b or failure_s:
            return True
        else:
            return False
        
    #this function will decode the beacon signal
    def DecodeSignal():
        return True

    #this function will return the commanded Power
    def Commaned_Power():
        return

    # Initialize the counter at the current time (in seconds)
    start_time = time.time()

    # To get the number of seconds that have passed since the start
    #def get_seconds_since_start():
        #return int(time.time() - start_time)

