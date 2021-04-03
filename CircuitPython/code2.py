
import board
import time
import random
import digitalio
import busio
#import adafruit_sdcard
import sdcardio
import storage
import adafruit_adxl34x
import adafruit_lsm9ds1
import os
from adafruit_debouncer import Debouncer


print("recording?")

# Set to false to disable testing/tracing code
TESTING = False

# Implementation dependant things to tweak

# Pins
SWITCH_PIN1 = board.D14
SWITCH_PIN2 = board.D15

LED_PIN = board.D13
################################################################################
# Setup hardware

# Setup a test switch connected to D14
switch_1 = digitalio.DigitalInOut(SWITCH_PIN1)
switch_1.direction = digitalio.Direction.INPUT
switch_1.pull = digitalio.Pull.UP
switch1 = Debouncer(switch_1)

# Setup a test switch connected to D15
switch_2 = digitalio.DigitalInOut(SWITCH_PIN2)
switch_2.direction = digitalio.Direction.INPUT
switch_2.pull = digitalio.Pull.UP
switch2 = Debouncer(switch_2)


# Setup a LED connected to D13 (led is smt on board)
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SD_SCK, MOSI=board.SD_MOSI, MISO=board.SD_MISO)
cs = board.SD_CS

sdcard = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


print(os.listdir("/sd/Saved_Data"))

#setup lsm9ds1 accel/gyro/mag combo
i2c = busio.I2C(board.SCL, board.SDA)
LSM1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)



# setup accelerometer - this is temp and will require code for multiple accels and the i2c multiplexer
#i2c = busio.I2C(board.SCL, board.SDA)
#i2c = busio.I2C(board.SCL, board.SDA)
#accelerometer = adafruit_adxl34x.ADXL345(i2c)



# Set the time for testing
# Once finished testing, the time can be set using the REPL using similar code
#if TESTING:
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    #t = time.struct_time((2018,  12,   31,   23,  58,  55,    1,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    #print("Setting time to:", t)
    #rtc.datetime = t
   # print()

################################################################################
# Global Variables

# Set the sampling rates of the sensors here in Hz

Rate_Center_Accel = 1/25
Rate_Center_Gyro =2
Rate_Center_Mag = 1/2
Rate_Center_Temp = 1/100

Data_Header_Names = ["time", "temp", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z", "mag_x", "mag_y", "mag_z"]
Data_Names = ["time", "temperature", "acceleration", "acceleration", "acceleration", "gyro", "gyro", "gyro", "magnetic", "magnetic", "magnetic"]
Rates = [1/10, Rate_Center_Temp, Rate_Center_Accel, Rate_Center_Accel, Rate_Center_Accel, Rate_Center_Gyro, Rate_Center_Gyro, Rate_Center_Gyro, Rate_Center_Mag, Rate_Center_Mag, Rate_Center_Mag]
Tuple_index = [0,0,0,1,2,0,1,2,0,1,2]
Sensor_On =[1,1,1,1,1,1,1,1,1,1,1]
Data_Logged = [0,0,0,0,0,0,0,0,0,0,0]

################################################################################
# Support functions

def log(s):
    """Print the argument if testing/tracing is enabled."""
    if TESTING:
        print(s)

def log_condition(i,sensor_name,sensor_variable,now,tuple_num,self):
        if i != 0 and (now - machine.time_past[i]) >= Rates[i]:
            log("I is:" + str(i))
            temp_list = [0]
            temp_tuple = getattr(sensor_name, sensor_variable)
            if isinstance(temp_tuple, map):
                log('in the loop')
                temp_tuple = list(temp_tuple)
                Data_Logged[i] = temp_tuple[tuple_num]
                self.count = self.count + 1
                machine.time_past[i] = time.monotonic()

            else:
                temp_list[0] = temp_tuple
                Data_Logged[i] = temp_list[tuple_num]
                self.count = self.count + 1
                machine.time_past[i] = time.monotonic()

        else:
            Data_Logged[i] = False







################################################################################
# State Machine

class StateMachine(object):

    def __init__(self):
        self.state = None
        self.states = {}
        self.Data_Values = []
        self.clocktime = time.monotonic()
        self.time_past = []
        self.filename = ""


    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Entering %s' % (self.state.name))
        self.state.enter(self)

    def update(self):
        if self.state:
            log('Updating %s' % (self.state.name))
            self.state.update(self)

    # When pausing, don't exit the state
    def pause(self):
        self.state = self.states['paused']
        print('Pausing')
        self.state.enter(self)

    # When resuming, don't re-enter the state
    def resume_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Resuming %s' % (self.state.name))






################################################################################
# States


# Abstract parent state class.

class State(object):

    def __init__(self):
        pass

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def update(self, machine):
        if switch2.fell:
                machine.paused_state = machine.state.name
                machine.pause()
                return False
        return True

# Wait for 10 seconds to midnight or the witch to be pressed,
# then drop the ball.

class IdleState(State):

    def __init__(self):
        super().__init__()
        self.entered1 = time.monotonic()
        led.value = False

    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)
        self.entered1 = time.monotonic()
        led.value = False
        print("in idle state")

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        if State.update(self, machine):
             if switch1.rose:
                print("recording started")
                machine.go_to_state('newfile')




#Handles saving of the final file and file system managment

class HandleState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'Handle'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)




#Creates a new CSV file and does file system managment

class NewFileState(State):

    def __init__(self):
        super().__init__()
        self.file_num = 1

    @property
    def name(self):
        return 'newfile'

    def enter(self, machine):
        State.enter(self, machine)
        self.file_num = 1

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)
        temp = "/sd/Saved_Data/data" + str(self.file_num) + ".csv"
        #this needs to be cleaned up
        try:
            if os.stat(temp):
                self.file_num = self.file_num + 1
        except:
            machine.filename = temp
            with open(machine.filename, "a") as file:
                log("saving data....")
                x = ""
                for i in range(len(Data_Header_Names)):
                    if i != len(Data_Header_Names):
                        x = x + "," + str(Data_Header_Names[i])
                    else:
                        x = x + Data_Header_Names[i]
                file.write(x + "\n")
            print(os.listdir("/sd/Saved_Data"))
            machine.go_to_state('log')





## LogState logs the data and then saves it to the global data array. It then goes to the write state

class LogState(State):

    def __init__(self):
        super().__init__()
        for i in range(len(Data_Names)):
            machine.time_past.append(time.monotonic())


    @property
    def name(self):
        return 'log'

    def enter(self, machine):
        State.enter(self, machine)
        machine.Data_Values = []
        self.count = 0
        log("entering log")



    def exit(self, machine):
        State.exit(self, machine)
        log("exiting log")


    def update(self, machine):
        State.update(self, machine)
        now = time.monotonic()
        for i in range(len(Data_Names)):
            log_condition(i,LSM1,Data_Names[i],now,Tuple_index[i],self)

        #else:
            #Data_Logged[i] = 1

        if self.count > 0:
            Data_Logged[0] = now
            log(Data_Logged)
            machine.go_to_state('save')








#SaveState saves all the data collected in the last iteration to the SD card

class SaveState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'save'

    def enter(self, machine):
        State.enter(self, machine)


    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)
        with open(machine.filename, "a") as file:
            log("saving data....")
            x = ""
            for i in range(len(Data_Logged)):
                if i != len(Data_Logged):
                    x = x + "," + str(Data_Logged[i])
                else:
                    x = x + str(Data_Logged[i])
            file.write(x + "\n")
        machine.go_to_state("transmit")


#Transmit State uses LORA to transmit the data

class TransmitState(State):

    def __init__(self):
        super().__init__()
        self.entered = time.monotonic()
        led.value = True

    @property
    def name(self):
        return 'transmit'

    def enter(self, machine):
        State.enter(self, machine)
        self.entered = time.monotonic()
        led.value = True
        log("Entering Transmit")


    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        machine.go_to_state('log')

#Transmit State uses LORA to transmit the data

class DisplayState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'display'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)


#Transmit State uses LORA to transmit the data

class CriticalState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'critical'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)


class PausedState(State):

    def __init__(self):
        super().__init__()
        self.switch_pressed_at = 0

    @property
    def name(self):
        return 'paused'

    def enter(self, machine):
        State.enter(self, machine)
        self.switch_pressed_at = time.monotonic()

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        if switch2.fell:
            machine.resume_state(machine.paused_state)
        elif not switch2.value:
            if time.monotonic() - self.switch_pressed_at > 1.0:
                machine.go_to_state('idle')


################################################################################
# Create the state machine


machine = StateMachine()

machine.add_state(IdleState())
machine.add_state(HandleState())
machine.add_state(NewFileState())
machine.add_state(LogState())
machine.add_state(SaveState())
machine.add_state(TransmitState())
machine.add_state(DisplayState())
machine.add_state(CriticalState())
machine.add_state(PausedState())



machine.go_to_state('idle')

while True:
    switch1.update()
    switch2.update()
    machine.update()