# This is the code to Transmit - set up for M4
import board
import busio
import time
import digitalio
import adafruit_rfm9x

# the default baudrate is 10MHz if we want to change it..
# Initialze RFM radio with a more conservative baudrate
# rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

# set the time interval (seconds) for sending packets
transmit_interval = 5

# Radio Frequency in MHz - can be changed
RADIO_FREQ_MHZ = 915.0

#initializes the SPI Bus
# Serial Peripheral Interface - a kind of synchronizing clock
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#initializes the pinouts
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

#Initializes the rfm radio object
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, RADIO_FREQ_MHZ, baudrate=5000000)

#Set the transmit power, the default is 13dB
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



# send startup message from my_node
rfm9x.send_with_ack(bytes("startup message from node {}".format(rfm9x.node), "UTF-8"))
rfm9x.send_with_ack(bytes("First Data Sequence:".format(rfm9x.node), "UTF-8"))
rfm9x.send_with_ack(bytes(str(test_list[0]).format(rfm9x.node), "UTF-8"))


#for x in range(0, length, 1):
 #   tosend = str(test_list[x])
  #  rfm9x.send(tosend)
   # print("Sending sequence!")
    #time.sleep(2)

# Wait to receive packets.
print("Waiting for packets...")
# initialize flag and timer
time_now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_ack=True, with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("RSSI: {0}".format(rfm9x.last_rssi))
        # send reading after any packet received
    if time.monotonic() - time_now > transmit_interval:
        # reset timer
        time_now = time.monotonic()
        counter += 1
        # send a  mesage to destination_node from my_node
        tosend = str(test_list[counter])
        if not rfm9x.send_with_ack(
            bytes(tosend.format(rfm9x.node, counter), "UTF-8")
        ):
            ack_failed_counter += 1
            print(" No Ack: ", counter, ack_failed_counter)