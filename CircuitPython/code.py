import board
import digitalio
import time
import adafruit_sdcard
import storage
import busio
import adafruit_adxl34x

# Setup the little red LED on D13
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# setup accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)


PULSE_TIME = 1
last_time = time.monotonic()



Data_Names = ["time","accel_x", "accel_y", "accel_z"]
Data_Values = []
print("Logging acceleration to SD card")

while True:
    if time.monotonic() - last_time >= PULSE_TIME:
        Data_Values = [time.monotonic(),accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]
        #print(*Data_Names, sep = ", ")
        #print(*Data_Values, sep = ", ")
        with open("/sd/data.csv", "a") as file:
            led.value = True
            accleration_x = accelerometer.acceleration[0]
            print("X acceleration = %0.0001f" % accleration_x)
            file.write(str(Data_Values[0]) + "," + str(Data_Values[1])  + "," + str(Data_Values[2])  + "," + str(Data_Values[3]) + "\n")
            led.value = False  # Turn off LED to indicate we're done
        last_time = time.monotonic()