# This is the code to Transmit - set up for M4
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
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# initializes the rfm radio object, using the adafruit_rfm9x class
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, radio_freq, baudrate = 5000000)

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
ack_failed_counter = 0

data = [1.0, 2.0, 2.5, 3.5, 4.5, 8.9, 9.120, 10, 13, 18, 21.5]
length = len(data)

# send startup message from my_node
rfm9x.send_with_ack(bytes("startup message from node {}".format(rfm9x.node), "UTF-8"))

# Wait to receive packets.
print("Waiting for packets...")

while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_ack=True, with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        #print("Received (raw header):", [hex(x) for x in packet[0:4]])
        #print("Received (raw payload): {0}".format(packet[4:]))
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