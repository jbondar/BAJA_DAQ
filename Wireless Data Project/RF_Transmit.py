import board
import busio
import digitalio
import adafruit_rfm9x

# the default baudrate is 10MHz if we want to change it..
# Initialze RFM radio with a more conservative baudrate
# rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

RADIO_FREQ_MHZ = 915.0      # We set this to what we want
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, RADIO_FREQ_MHZ, baudrate=5000000)

test_list = [42.0, 69.6, 666]

rfm9x.send(bytes(test_list[0]))
print("Sending first sequence")