import digitalio
import board
import busio
import adafruit_rfm9x

LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# The default baudrate is 5Mhz
RADIO_FREQ_MHZ = 915.0
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, RADIO_FREQ_MHZ)

while True:
    packet = rfm9x.receive()
    if packet is None:
        LED.value = False
        print("You get NOTHING! Perhaps try again..")
    else:
        LED.value = True
        print("Received (raw bytes): {0}".format(packet))