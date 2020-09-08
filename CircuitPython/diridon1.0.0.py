#libraries needed for the sdcard and the accelerometer
import time
import adafruit_sdcard
import microcontroller
import board
import busio
import digitalio
import storage
import adafruit_adxl34x

# Create iC2 object
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize the iC2 connection with the breakout
accelerometer = adafruit_adxl34x.ADXL343(i2c)

# Setup the little red LED on D13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

print("Logging acceleration to SD card")
# We're going to append to the file
while True:
    # Open file for append
    with open("/sd/acceleration.txt", "a") as file:
        led.value = True  # Turn on LED to indicate we're writing to the file
        accelerometer= adafruit_adxl34x.ADXL345(i2c)
        print(accelerometer.acceleration)
        file.write(accelerometer.acceleration)
        led.value = False  # Turn off LED to indicate we're done
    # File is saved
    time.sleep(0.2)