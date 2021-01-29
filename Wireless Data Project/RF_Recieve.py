# Code for Receiving Node (M4)
import digitalio
import board
import busio
import adafruit_rfm9x
import struct
import time

# unpack_data converts byte array to double
def unpack_data(data_to_unpack):
    # Pull the number of encoded items (Note a tuple is returned!)
    elen = struct.unpack_from("!I", data_to_unpack)[0]
    # Now pull the array of items
    arr = struct.unpack_from("!" + "d" * elen, data_to_unpack, 4)
    return arr

# led pinouts definitions
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# The default baudrate is 5Mhz - matches transmitting baudrate
# Defines the Radio Frequency
radio_freq = 915.0

# initializes the SPI Bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# initializes the pinouts
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq, baudrate=5000000)

# enable CRC checking
rfm9x.enable_crc = True

# set node addresses
rfm9x.node = 2
rfm9x.destination = 1

while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        led.value = True
        # Received a packet!
        print("RSSI: {0}".format(rfm9x.last_rssi))
        # WARNING! Always exclude the 1st 4 bytes of data from packet!
        data = unpack_data(packet[4:])
        print("Received Packet:", data)
    else:
        led.value = False