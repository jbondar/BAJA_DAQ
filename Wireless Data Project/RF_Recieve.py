# Code for Receiving Node (M4)
import time
import digitalio
import board
import busio
import adafruit_rfm9x

# Initializes on board LED for checking purposes
LED = digitalio.DigitalInOut(board.D13)
LED.direction = digitalio.Direction.OUTPUT

# The default baudrate is 5Mhz - matches transmitting baudrate
# Defines the Radio Frequency
radio_freq = 915.0

# initializes the SPI Bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# initializes the pinouts
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq, baudrate = 5000000)

# enable CRC checking
rfm9x.enable_crc = True

# set delay before transmitting ACK (seconds)
rfm9x.ack_delay = 0.1

# set node addresses
rfm9x.node = 2
rfm9x.destination = 1

# Creates counters for sending and ack failure
counter = 0
ack_failed_counter = 0

while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_ack=True, with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("RSSI: {0}".format(rfm9x.last_rssi))
        # send response 1/2 sec after any packet received
        #time.sleep(0.5)
        counter += 1
        # send a  mesage to destination_node from my_node
        if not rfm9x.send_with_ack(
            bytes("response from node {} {}".format(rfm9x.node, counter), "UTF-8")
        ):
            ack_failed_counter += 1
            print("No Ack: ", counter, ack_failed_counter)