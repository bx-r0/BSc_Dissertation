## This iptable command needs to be run to push all packets into the NFQUEUE
#----------------------------------------#
# "sudo iptables -A INPUT -j NFQUEUE"
#----------------------------------------#

import time
from scapy.all import *
from netfilterqueue import NetfilterQueue


def print_packet(packet):
    print("[!] ", end='')
    print(packet)


def edit_packet(packet):
    # Converts into Scapy compatable string
    pkt = IP(packet.get_payload())

    # ------------------ #
    # EDIT PACKET HERE
    # ------------------ #

    # Sets the packet to the modified version
    packet.set_payload(bytes(pkt))

    # Accepts and lets the packet leave the queue
    packet.accept()


def latency(packet):
    # Used to debug
    print_packet(packet)

    # Issues latency of one second
    time.sleep(1)
    packet.accept()


# Creates the object
nfqueue = NetfilterQueue()

# 0 is the default NFQUEUE and print_packet is the
nfqueue.bind(0, latency)

try:
    print("[*] Waiting ")
    nfqueue.run()
except KeyboardInterrupt:
    pass
