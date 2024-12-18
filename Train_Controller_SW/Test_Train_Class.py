
from PyQt6.QtCore import Qt, QTimer, QElapsedTimer



############################
#  Variable Declaration 
############################

#Bools
class Train_Controller:

    #train constructor function
    def __init__ (self, id):
    

        self.is_micah = True
        self.manual_mode = False
        self.e_brake = False
        self.s_brake = False
        self.prev_s_brake = False
        self.r_door = False
        self.l_door = False
        self.i_light = False
        self.o_light = False
        self.in_tunnel = False
        self.failure_engine = False
        self.failure_brake = False
        self.failure_signal = False
        self.station_reached = False
        self.doors_can_open = False
        self.can_get_authority = True

        #Floats
        self.k_p = 7000
        self.k_i = 50
        self.time_world = 0.0
        self.commanded_power = 0.0
        self.ek = 0.0
        self.ek_1 = 0.0
        self.T = 0.09 #time samples of 90 ms
        self.uk = 0.0
        self.uk_1 = 0.0
        self.auth_diff = 0.0

        #Ints
        self.received_authority = 0
        self.authority = 0
        self.actual_velocity = 0
        self.commanded_velocity = 0
        self.setpoint_velocity = 0
        self.temperature = 68
        self.beacon_info = 0
        self.train_id = id
        self.doors_to_open = "0"

        self.sim_speed = 1
        self.elapsed_timer = QElapsedTimer()  #To track elapsed time

        #Strings
        self.pa_announcement = ""
        self.station_name = ""

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

        self.auth_diff_dict = {
            "auth_diff": self.auth_diff,
            "train_id": self.train_id
        }

        #Timer Initilization for both doors
        self.l_door_timer = QTimer()
        self.l_door_timer.setSingleShot(True)
        self.l_door_timer.timeout.connect(self.close_l_door)

        self.r_door_timer = QTimer()
        self.r_door_timer.setSingleShot(True)
        self.r_door_timer.timeout.connect(self.close_r_door)



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

        #if doors are closing, then we should now be able to get authority
        if left == False and self.authority <= 0:
            self.can_get_authority = True
            self.set_pa_announcement("Leaving " + self.station_name)    #announce leaving station

        self.l_door = left
        self.doors_dict["l_door"] = self.l_door

    def set_r_door(self, right):

        #if doors are closing, then we should now be able to get authority
        if right == False and self.authority <= 0:
            self.can_get_authority = True
            self.set_pa_announcement("Leaving " + self.station_name)    #announce leaving station


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

    def set_doors_can_open(self, can_open):
        self.doors_can_open = can_open

    #set temperature
    def set_temperature(self, temp):
        self.temperature = temp
        self.temperature_dict["temperature"] = self.temperature

        
    #set brakes
    def set_s_brake(self, status):
        old_brake = self.s_brake
        self.s_brake = status
        self.brakes_dict["s_brake"] = self.s_brake

        #print(f"Different: {old_brake != self.s_brake}")
        #only sends a new state if a change occurs
        #if self.is_micah and old_brake != self.s_brake:


    def set_e_brake(self, status):
        self.e_brake = status
        self.brakes_dict["e_brake"] = self.e_brake


    def set_pa_announcement(self, announcement):
        self.pa_announcement = announcement
        self.pa_announcement_dict["pa_announcement"] = self.pa_announcement


    #set authority
    def set_authority(self, distance):
        self.authority = distance

    def set_received_authority(self, distance):
        self.received_authority = distance

    def send_auth_diff(self):
        # try:
        #     if self.is_micah:
        #         #print("")
        #         response = requests.post(URL + "/track-model/get-data/auth_difference", json=self.auth_diff_dict)
        #         response.raise_for_status()  # This will raise an error for 4xx/5xx responses

        #         #print("Success:", response.json())

        # except requests.exceptions.HTTPError as http_err:
        #     # Print the HTTP error response
        #     print(f"HTTP error occurred: {http_err}")  # HTTP error details
        #     print("Response content:", response.text)   # Full response content

        # except Exception as err:
        # # Catch any other exceptions
        #     print(f"Other error occurred: {err}")

        # print(f"Difference: {self.auth_diff}")
        # print(f"Current Authority: {self.authority}")
        self.set_auth_diff(0)
        

    #set velocities
    def set_actual_velocity(self, v):
        self.actual_velocity = v
        self.update_authority()

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
        if power > 120000:
            power = 120000
            
        self.commanded_power = power

        self.commanded_power_dict["commanded_power"] = self.commanded_power

    #set failure modes
    def set_failure_engine(self, truth):
        self.failure_engine = truth

    def set_failure_brake(self, truth):
        self.failure_brake = truth

    def set_failure_signal(self, truth):
        self.failure_signal = truth

    def set_can_get_authority(self, truth):
        self.can_get_authority = truth

    def set_auth_diff(self, auth):
        self.auth_diff = auth
        self.auth_diff_dict["auth_diff"] = self.auth_diff

    def add_auth_diff(self, auth):
        self.auth_diff += auth
        self.auth_diff_dict["auth_diff"] = self.auth_diff

    def set_train_id(self, number):
        self.train_id = number

    def set_T(self, speed):
        self.T = .09/speed

    ############################
    #  Get Functions 
    ############################

    def get_train_id(self):
        return self.train_id

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
    
    def get_received_authority(self):
        return self.received_authority

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
    
    def get_doors_can_open(self):
        return self.doors_can_open
    
    def get_doors_to_open(self):
        return self.doors_to_open
    
    def get_can_get_authority(self):
        return self.can_get_authority
    

    #checks if authority is at distance where braking should occur in auto mode
    def stop_at_station(self):

        #checks if authorirt is less than Vi^2 / 2*max-braking
        if self.authority <= self.actual_velocity**2 / 2.4:
            self.set_s_brake(True)
            return True
        else:
            self.set_s_brake(False)
            return False
    
    #this function is called when we need to set authority to the authority sent us 
    def set_authority_to_received(self):
        self.set_authority(self.received_authority + self.authority) #adds to compensate for overshooting station by a little
        
    #this function updates authority in real time in order to have an accurate reading for the driver
    def update_authority(self):
        self.authority -= self.actual_velocity*.09   #multiple time interval by actual velocity
        self.add_auth_diff(self.actual_velocity*.09)


    #this function will return the setpoint velocity based on the commaned velocity and user inputed set point velocity
    #if the user inputs a value higher than commaned velocity, the set point will default to the commanded velocity
    def SetSetPointVelocity(self):
        if float(self.setpoint_velocity) > float(self.commanded_velocity):
            self.setpoint_velocity = self.commanded_velocity

    #this function will decode the beacon signal
    def decode_signal(self):
        
        #split signal in 3 segments
        values = self.beacon_info.split(',')


        if len(values) == 1:
            #check if tunnel beacon
            if values[0][0] == "T" or values[0][0] == "t":
                self.in_tunnel = not(self.in_tunnel)    #flip in_tunnel bool

                #turn lights on if in tunnel
                if self.in_tunnel:
                    self.set_i_light(True)
                    self.set_o_light(True)
                else:
                    self.set_i_light(False)
                    self.set_o_light(False)
        #this decodes the 3 segments of information
        elif len(values) == 3:

            #checks if station beacon
            if values[0][0] == "B" or "b":
                self.station_reached = not(self.station_reached)

                #checks if it is shared tunnel station block
                if len(values[0]) == 3:


                    if values[0][1] == "3" and values[0][2] == "1":
                        self.in_tunnel = not(self.in_tunnel)

                        #turn lights on if in tunnel
                        if self.in_tunnel:
                            self.set_i_light(True)
                            self.set_o_light(True)
                        else:
                            self.set_i_light(False)
                            self.set_o_light(False)


                #checks if station is reached and authority is low enough (166.1m: put in 200 m for error for now)
                if self.station_reached and self.authority < 200:
                    self.doors_can_open = True

                    #check which doors open
                    self.doors_to_open = values[1]

                    #set pa announcement string
                    self.station_name = values[2]
                    self.set_pa_announcement("Arriving at " + self.station_name)

    #this function will return the commanded Power and will be called every 50 ms
    def calculate_commanded_power(self):

        #check setpoint speed first or if any brakes are being pressed
        if self.setpoint_velocity <= self.actual_velocity or (self.s_brake and not self.failure_brake) or self.e_brake or self.authority <= 0:
            self.set_commanded_power(0)
            self.ek = 0
            self.ek_1 = 0
            self.uk = 0
            self.uk_1 = 0



            # if self.is_micah:
            #     try:
            #         response = self.session.post(URL + "/train-model/receive-commanded-power", json=self.commanded_power_dict, timeout = 5)
            #         self.session.close()
            #     except requests.exceptions.ConnectionError as e:
            #         print("Connection error:", e)

            #self.train_model_list[self.train_id].set_commanded_power(self.commanded_power)

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

        #print(f"Commanded Power: {self.commanded_power}")

        # if self.is_micah:
        #     try:
        #         response = self.session.post(URL + "/train-model/receive-commanded-power", json=self.commanded_power_dict, timeout = 5)
        #         self.session.close()
        #     except requests.exceptions.ConnectionError as e:
        #         print("Connection error:", e)

        #self.train_model_list[self.train_id].set_commanded_power(self.commanded_power)

    def open_l_door(self, sim_speed):
        self.set_l_door(True)
        self.elapsed_timer.start()
        self.sim_speed = sim_speed
        #self.set_doors_can_open(False)

        #JUST IN CURRENT
        # self.l_door_button.setEnabled(False)
        # self.l_door_button.setText("Opened")

        #start 60s timer (divides by sim speed to account for simulation time)
        self.l_door_timer.start(int(60000/sim_speed))

    def open_r_door(self, sim_speed):
        self.set_r_door(True)
        self.elapsed_timer.start()
        self.sim_speed = sim_speed
        #self.set_doors_can_open(False)

        #JUST IN CURRENT
        # self.r_door_button.setEnabled(False)
        # self.r_door_button.setText("Opened")

        #start 60s timer (divides by sim speed to account for simulation time)
        self.r_door_timer.start(int(60000/sim_speed))

    def close_l_door(self):
        #door is now closed
        self.set_l_door(False)

        #ONLY IN CURRENT
        # self.l_door_button.setText("Closed")

        # #activates door button again if in manual mode (ONLY IN CURRENT)
        # if self.train_list[self.current_train].get_manual_mode():
        #     self.l_door_button.setEnabled(True)

    def close_r_door(self):
        #door is now closed
        self.set_r_door(False)

        #ONLY IN CURRENT
        # self.r_door_button.setText("Closed")

        # #activates door button again if in manual mode (ONLY IN CURRENT)
        # if self.train_list[self.current_train].get_manual_mode():
        #     self.r_door_button.setEnabled(True)


    #called when sim_speed is changed
    def adjust_door_timer(self, new_sim_speed):
        if self.r_door_timer.isActive() or self.l_door_timer.isActive():

            #Stop the timer and calculate elapsed time in simulation
            elapsed_real_time = self.elapsed_timer.elapsed() 
            elapsed_sim_time = elapsed_real_time * self.sim_speed  

            #Calculate remaining time in real-time
            remaining_time = max(0, 60000 - elapsed_sim_time)

            #Update simulation speed and restart the timer with adjusted time
            self.sim_speed = new_sim_speed

            #checks which door is active
            if self.r_door_timer.isActive():
                self.r_door_timer.start(int(remaining_time / self.sim_speed))
            
            if self.l_door_timer.isActive():
                self.l_door_timer.start(int(remaining_time / self.sim_speed))

            self.elapsed_timer.restart()

