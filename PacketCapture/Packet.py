import getopt

from netfilterqueue import NetfilterQueue
from scapy.all import *

"""
This iptables command needs to be run to push all packets into the NFQUEUE:

        "sudo iptables -A INPUT -j NFQUEUE"

To restore full internet connection run:

        "sudo iptables -F"
"""
def print_force(string):
    print(string)
    sys.stdout.flush()


def affect_packet(packet):
    """This function checks if the packet should be affected or not"""

    if target_packet_type == "ALL":
        return True
    else:
        # Grabs the first section of the Packet
        packet_string = str(packet)
        split = packet_string.split(' ')

        # Checks for the target packet type
        if target_packet_type == split[0]:
            return True
        else:
            return False


def ignore_packet(packet):
    """This is just used a default 'do nothing' function """

    # Accepts and lets the packet leave the queue
    packet.accept()


def print_packet(packet):
    """This function just prints the packet"""

    if affect_packet(packet):
        print_force("[!] " + str(packet))

    # Accepts and lets the packet leave the queue
    packet.accept()


def edit_packet(packet):
    """This function will be used to edit sections of a packet, this is currently incomplete"""

    if affect_packet(packet):
        # Converts into Scapy compatible string
        pkt = IP(packet.get_payload())

        # TODO: Packet editing here

        # Sets the packet to the modified version
        packet.set_payload(bytes(pkt))

    # Accepts and lets the packet leave the queue
    packet.accept()


def packet_latency(packet):
    """This function is used to incur latency on packets"""

    # TODO: Issues with ^c not working when latency is active
    if affect_packet(packet):
        # Shows the packet
        print_force("[!] " + str(packet))

        # Issues latency of the entered value
        time.sleep(latency_value_second)

    # Accepts and lets the packet leave the queue
    packet.accept()


def packet_loss(packet):
    """This function will issue a packet loss,
    a percentage is defined and anything
    lower is dropped and anything else is accepted"""

    if affect_packet(packet):
        # random value from 1 to 100
        random_value = random.uniform(1, 100)

        # If the generated value is smaller than the percentage discard
        if packet_loss_percentage > random_value:
            packet.drop()
            print_force("[!] Packet dropped!")
        # Accept the packet
        else:
            packet.accept()
    # This else is needed because the packet would be blocked if it's not the target
    else:
        packet.accept()


def run_packet_manipulation():
    """The main method here, will issue a iptables command and construct the NFQUEUE"""

    try:
        # Runs the IPTABLES command
        os.system("iptables -A INPUT -j NFQUEUE")

        print_force("[*] Mode is: " + mode.__name__)

        # Setup for the NQUEUE
        nfqueue = NetfilterQueue()

        try:
             nfqueue.bind(0, mode)  # 0 is the default NFQUEUE
        except OSError:
            print_force("[!] Queue already created")

        # Shows the start waiting message
        print_force("[*] Waiting ")
        nfqueue.run()

    except (KeyboardInterrupt, SystemExit):
        print("\n[!] Process aborted")
        print("[!] iptables reverted")
        os.system("iptables -F")


def usage():
    """Issues a terminal help message"""

    print("""
    Options:
    #=================================================#
    |-p                             - Print packet    |
    |-e                             - Packet edit     |
    |-l <latency_seconds>           - Latency         |
    |-z <loss_percentage>           - Packet loss     |
    |-t <target_packet_protocol>    - Target protocol |
    |-h                             - Help            |
    #=================================================#
    """)


def parameters():
    """This function deals with parameters passed to the script
    most of the handling is performed by the 'getopt' module"""

    # Defines globals to be used above
    global mode
    global latency_value_second
    global packet_loss_percentage
    global target_packet_type

    try:
        # The 2nd parameter for getopt() specifies the expected parameters
        # "p"   = "-p"
        # "t:"  = "-t <value>" Note: ":" is used to specify a value will preced
        opts, args = getopt.getopt(sys.argv[1:], 'pel:z:ht:', '')

        for opt, arg in opts:
            # ---------- Flags ---------- # - Parameters without values
            if opt == "-h":
                usage()
                sys.exit(0)

            elif opt == "-p":
                mode = print_packet

            # ---------- Arguments ---------- # - Parameters with values
            elif opt == "-l":
                mode = packet_latency
                latency_value_second = int(arg) / 1000

            elif opt == "-z":
                mode = packet_loss
                packet_loss_percentage = int(arg)

            elif opt == "-t":
                print_force("[!] Only affecting " + arg + " packets")
                target_packet_type = arg

        # When all parameters are handled
        run_packet_manipulation()

    except getopt.GetoptError:
        print_force("Error: incorrect parameters")
        usage()
        sys.exit(2)

# ------------------------DEFINITION END ------------------------------ #


# Default value
packet_loss_percentage = 0
latency_value_second = 0
mode = ignore_packet
target_packet_type = "ALL"

# Check if user is root
if os.getuid() != 0:
    exit("Error: User needs to be root to run this script")

# Parameter handling
parameters()
