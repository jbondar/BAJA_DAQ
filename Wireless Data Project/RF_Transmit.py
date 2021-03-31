# This is the code to Transmit - M4
import board
import busio
import time
import digitalio
import adafruit_rfm9x
import struct

# pack_data converts the data_to_pack to a byte array
def pack_data(data_to_pack):
    # First encode the number of data items, then the actual items
    ba = struct.pack("!I" + "d" * len(data_to_pack),
                    len(data_to_pack), *data_to_pack)
    return ba

# sendData sends the converted data to our 2nd node
def sendData(data):
    # checks to see if data is null
    if data:
        ts = pack_data(data)
        rfm9x.send(ts)


# radio frequency in MHz
radio_freq = 915.0

# initializes the SPI Bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# initializes the pinouts
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)
# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq)

# set the transmit power, default is 13dB
rfm9x.tx_power = 23

# enable CRC checking
rfm9x.enable_crc = True

# set node addresses
rfm9x.node = 1
rfm9x.destination = 2

# below this point is for testing purposes and
# will need to be changed when integrated into master

# Test array
data = [[0, 45.5, 2.23], [1, 45.5, 2.23],
        [2, 45.5, 2.23], [3, 45.5, 2.23],
        [4, 45.5, 2.23], [5, 45.5, 2.23],
        [6, 45.5, 2.23], [7, 45.5, 2.23], [8, 45.5, 2.23]]

cntr = 0

# Loops thru array & sends by calling sendData
while True:
    sendData(data[cntr])
    cntr += 1
    if (cntr == len(data)): cntr = 0