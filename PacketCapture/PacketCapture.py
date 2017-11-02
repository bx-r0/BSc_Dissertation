"""
This iptables command needs to be run to push all packets into the NFQUEUE:

        "sudo iptables -A INPUT -j NFQUEUE"

To restore full internet connection run:

        "sudo iptables -F"
"""
from scapy.all import *
from netfilterqueue import NetfilterQueue
from Window import PacketCaptureGTK


def print_packet(packet):
    print("[!] ", end='')
    print(packet)


def edit_packet(packet):
    # Converts into Scapy compatible string
    pkt = IP(packet.get_payload())

    # Sets the packet to the modified version
    packet.set_payload(bytes(pkt))

    # Accepts and lets the packet leave the queue
    packet.accept()


def packet_latency(packet):
    # Used to debug
    print_packet(packet)

    # Issues latency of one second
    time.sleep(latency_value_second)
    packet.accept()


def packet_loss(packet):
    # random value from 1 to 100
    random_value = random.uniform(1, 100)

    # If the generated value is smaller than the percentage discard
    if packet_loss_percentage > random_value:
        packet.drop()
        print("[!] Packet dropped!")
    # Accept the packet
    else:
        packet.accept()


def run():
    try:
        # Prints the mode the program is running in
        print("[*] Mode is: ", end='')
        print(mode.__name__)

        # Shows the start waiting message
        print("[*] Waiting ")
        nfqueue.run()
    except KeyboardInterrupt:
        pass


# -------VARIABLES---------- #
mode = print_packet  # <-- Change this variable to change the network degradation type

# Degradation characteristic
packet_loss_percentage = 10
latency_value_second = 1
# -------------------------- #

# Loads up the packet window
packet_window = PacketCaptureGTK()

# Setup for the NQUEUE
nfqueue = NetfilterQueue()
nfqueue.bind(0, mode)  # 0 is the default NFQUEUE







