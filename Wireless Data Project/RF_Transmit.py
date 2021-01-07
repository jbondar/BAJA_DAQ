# This is the code to Transmit - set up for M4
import board
import busio
import time
import digitalio
import adafruit_rfm9x

# set the time interval (seconds) for sending packets
transmit_interval = 5

# radio frequency in MHz
radio_freq = 915.0

# initializes the SPI Bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# initializes the pinouts
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# sets a baudrate
baudrate = 5000000

# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq, baudrate)

# set the transmit power, default is 13dB
rfm9x.tx_power = 23

# enable CRC checking
rfm9x.enable_crc = True

# set delay before sending ACK
rfm9x.ack_delay = 0.1

# set node addresses
rfm9x.node = 1
rfm9x.destination = 2

# initialize counter
counter = 0
ack_failed_counter = 0

test_list = [1.0, 2.0, 3.0, 2.5, 4.5, 8.9, 9.120]
length = len(test_list)

# initialize flag and timer
time_now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_ack=True, with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet: note to self what does this return
        print("Received (raw payload): {0}".format(packet[4:]))
        print("RSSI: {0}".format(rfm9x.last_rssi))
        # send reading after any packet received
    if time.monotonic() - time_now > transmit_interval:
        # send a  mesage to destination_node from my_node
        tosend = str(test_list[counter])
        # reset timer
        time_now = time.monotonic()
        counter += 1
        if not rfm9x.send_with_ack(
            bytes(tosend.format(rfm9x.node, counter), "UTF-8")
            ):
            ack_failed_counter += 1
            print(" No Acknowledgement: ", counter, ack_failed_counter)