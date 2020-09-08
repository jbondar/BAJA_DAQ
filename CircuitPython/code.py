import board
import digitalio
import time
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)

accelerometer = adafruit_adxl34x.ADXL345(i2c)


PULSE_TIME = 1
last_time = time.monotonic()



Data_Names = ["time","accel_x", "accel_y", "accel_z"]
Data_Values = []
while True:
    if time.monotonic() - last_time >= PULSE_TIME:
        Data_Values = [time.monotonic(),accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]
        print(*Data_Names, sep = ", ")
        print(*Data_Values, sep = ", ")
        last_time = time.monotonic()


