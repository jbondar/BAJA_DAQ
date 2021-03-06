
# Setup a test switch connected to D9
import board
import time
import random
import digitalio
import busio
#import adafruit_sdcard
import adafruit_rfm9x
import struct
import storage
#import adafruit_adxl34x

print("Hello, world!")



# Set to false to disable testing/tracing code
TESTING = False

# Implementation dependant things to tweak


# Pins
#SWITCH_PIN = board.D9
LED_PIN = board.D13
################################################################################
# Setup hardware

# Setup a test switch connected to D9
#switch_io = digitalio.DigitalInOut(SWITCH_PIN)
#switch_io.direction = digitalio.Direction.INPUT
#switch_io.pull = digitalio.Pull.UP
#switch = Debouncer(switch_io)

# Setup a LED connected to D13 (led is smt on board)
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
#spi = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)
#cs = digitalio.DigitalInOut(board.SD_CS)
#sdcard = adafruit_sdcard.SDCard(spi, cs)
#vfs = storage.VfsFat(sdcard)
#storage.mount(vfs, "/sd")

# setup accelerometer - this is temp and will require code for multiple accels and the i2c multiplexer
#i2c = busio.I2C(board.SCL, board.SDA)
#i2c = busio.I2C(board.SCL, board.SDA)
#accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Set the time for testing
# Once finished testing, the time can be set using the REPL using similar code
if TESTING:
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2018,  12,   31,   23,  58,  55,    1,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)
    rtc.datetime = t
    print()

################################################################################
# Global Variables
Data_Names = ["time", "accel_x", "accel_y", "accel_z"]

# Lora Info
radio_freq = 915.0
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# Test array
dtt = [[0, 45.5, 2.23], [1, 45.5, 2.23],
        [2, 45.5, 2.23], [3, 45.5, 2.23],
        [4, 45.5, 2.23], [5, 45.5, 2.23],
        [6, 45.5, 2.23], [7, 45.5, 2.23], [8, 45.5, 2.23]]

################################################################################
# Support functions

def log(s):
    """Print the argument if testing/tracing is enabled."""
    if TESTING:
        print(s)





################################################################################
# State Machine

class StateMachine(object):

    def __init__(self):
        self.state = None
        self.states = {}
        self.Data_Values = []


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
        log('Pausing')
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
        #if switch.fell:
         #   machine.paused_state = machine.state.name
          #  machine.pause()
          #  return False
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

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):

        if State.update(self, machine):
            now = time.monotonic()
            if now - self.entered1 >= 3.0:
                print("in idle")

                led.value = True
                machine.go_to_state('log')




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

    @property
    def name(self):
        return 'newfile'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)




## LogState logs the data and then saves it to the global data array. It then goes to the write state

class LogState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'log'

    def enter(self, machine):
        State.enter(self, machine)
        machine.Data_Values = [1, 2, 3, 4]


    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)
        machine.go_to_state('transmit')


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
        with open("/sd/data.csv", "a") as file:
            print("saving data....")
            file.write(str(machine.Data_Values[0]) + "," + str(machine.Data_Values[1])  + "," + str(machine.Data_Values[2])  + "," + str(machine.Data_Values[3]) + "\n")
        machine.go_to_state("transmit")


#Transmit State uses LORA to transmit the data

# IGNORE THIS
#rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq)
#rfm9x.tx_power = 23
#rfm9x.enable_crc = True
#rfm9x.node = 1
#rfm9x.destination = 2

class TransmitState(State):

    def __init__(self):
        super().__init__()
        self.entered = time.monotonic()
        self.rf = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq)
        self.rf.tx_power = 23
        self.rf.enable_crc = True
        self.rf.node = 1
        self.rf.destination = 2
        led.value = True

# converts data to byte array - Lora
    def pack_data(self, data_to_pack):
        # First encode the number of data items, then the actual items
        ba = struct.pack("!I" + "d" * len(data_to_pack),
                    len(data_to_pack), *(data_to_pack))
        return ba

# sendData sends the converted data to our 2nd node
    def sendData(self, data):
    # checks to see if data is null
        if data:
            if type(data) == str:
                self.rf.send(data)
            else:
                ts = self.pack_data(data)
                self.rf.send(ts)


    @property
    def name(self):
        return 'transmit'

    def enter(self, machine):
        State.enter(self, machine)
        self.entered = time.monotonic()
        led.value = True
        print("Entering Transmit")

    def exit(self, machine):
        print("Exiting Transmit")
        State.exit(self, machine)

    def update(self, machine):

        if State.update(self, machine):
            now = time.monotonic()
            if now - self.entered >= 1.0:
                led.value = False
                print("Transmitting...")
                self.sendData(dtt[3])
                machine.go_to_state('idle')


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


print("hello")

machine.go_to_state('idle')

while True:
    machine.update()
    time.sleep(.5)