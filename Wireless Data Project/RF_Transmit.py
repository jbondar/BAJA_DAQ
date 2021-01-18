# This is the code to Transmit - M0
import board
import busio
import time
import digitalio
import adafruit_rfm9x

# radio frequency in MHz
radio_freq = 915.0

# initializes the SPI Bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# initializes the pinouts
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)

# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq)

# set the transmit power, default is 13dB
rfm9x.tx_power = 23

# enable CRC checking
rfm9x.enable_crc = True

# set delay before sending ACK
# rfm9x.ack_delay = 0.2

# Sets num of retries
rfm9x.ack_retries = 2

# set node addresses
rfm9x.node = 1
rfm9x.destination = 2

# initialize counter
ack_failed_counter = 0

data = [['s1', 45.5, 2.23], ['s2', 45.5, 2.23],['s3', 45.5, 2.23],['s4', 45.5, 2.23],['g', 45.5, 2.23]]

# send startup message from my_node
rfm9x.send_with_ack(bytes("startup message from node {}".format(rfm9x.node), "UTF-8"))

while True:
    # Look for a new packet: only accept if addresses to my_node
    # If no packet was received during the timeout then None is returned.
    packet = rfm9x.receive(with_ack=True, with_header=True)

    # This statement checks if list is empty before sending
    if data:
        if (packet is not None):
        # Received a packet!
        # Print out the RSSI
            print("RSSI: {0}".format(rfm9x.last_rssi))
            tosend = str(data[0])
            if rfm9x.send_with_ack(
                bytes(tosend.format(rfm9x.node), "UTF-8")
            ):
                print("Sent: ", data[0])
                data.pop(0)
                ack_failed_counter = 0
            else:
                ack_failed_counter += 1
                print("No Ack: ", counter, ack_failed_counter)
