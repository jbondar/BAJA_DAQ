import board
import digitalio
import time
import adafruit_sdcard
import storage
import busio
import adafruit_adxl34x


# Set to false to disable testing/tracing code
TESTING = False

# Implementation dependant things to tweak
NUM_PIXELS = 8               # number of neopixels in the striup
DROP_THROTTLE = -0.2         # servo throttle during ball drop
DROP_DURATION = 10.0         # how many seconds the ball takes to drop
RAISE_THROTTLE = 0.3         # servo throttle while raising the ball
FIREWORKS_DURATION = 60.0    # how many second the fireworks last

# Pins
NEOPIXEL_PIN = board.D5
POWER_PIN = board.D10
SWITCH_PIN = board.D9
SERVO_PIN = board.A1

################################################################################
# Setup hardware

# Power to the speaker and neopixels must be enabled using this pin

enable = digitalio.DigitalInOut(POWER_PIN)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(i2c)

audio = audioio.AudioOut(board.A0)

strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)
strip.fill(0)                          # NeoPixels off ASAP on startup
strip.show()

switch_io = digitalio.DigitalInOut(SWITCH_PIN)
switch_io.direction = digitalio.Direction.INPUT
switch_io.pull = digitalio.Pull.UP
switch = Debouncer(switch_io)

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(SERVO_PIN, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
servo = servo.ContinuousServo(pwm)
servo.throttle = 0.0

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

    def reset_fireworks(self):
        """As indicated, reset the fireworks system's variables."""
        self.firework_color = random_color()
        self.burst_count = 0
        self.shower_count = 0
        self.firework_step_time = time.monotonic() + 0.05
        strip.fill(0)
        strip.show()




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
        if switch.fell:
            machine.paused_state = machine.state.name
            machine.pause()
            return False
        return True

# Wait for 10 seconds to midnight or the witch to be pressed,
# then drop the ball.

class IdleState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'idle'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)



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

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)



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


#Transmit State uses LORA to transmit the data

class TransmitState(State):

    def __init__(self):
        super().__init__()

    @property
    def name(self):
        return 'transmit'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        State.update(self, machine)



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



machine.go_to_state('waiting')

while True:
    switch.update()
    machine.update()