from netfilterqueue import NetfilterQueue
from scapy.all import *

"""
This iptables command needs to be run to push all packets into the NFQUEUE:

        "sudo iptables -A INPUT -j NFQUEUE"

To restore full internet connection run:

        "sudo iptables -F"
"""


def ignore_packet(packet):
    """This is just used a default 'do nothing' function """

    packet.accept()


def print_packet(packet):
    """This function just prints the packet"""

    print("[!] ", end='')
    print(packet)
    packet.accept()


def edit_packet(packet):
    """This function will be used to edit sections of a packet, this is currently incomplete"""

    # Converts into Scapy compatible string
    pkt = IP(packet.get_payload())

    # TODO: Packet editing here

    # Sets the packet to the modified version
    packet.set_payload(bytes(pkt))

    # Accepts and lets the packet leave the queue
    packet.accept()


def packet_latency(packet):
    """This function is used to incur latency on packets"""

    # Shows the packet
    print(packet)

    # Issues latency of the entered value
    time.sleep(latency_value_second)

    packet.accept()


def packet_loss(packet):
    """This function will issue a packet loss,
    a percentage is defined and anything
    lower is dropped and anything else is accepted"""

    # random value from 1 to 100
    random_value = random.uniform(1, 100)

    # If the generated value is smaller than the percentage discard
    if packet_loss_percentage > random_value:
        packet.drop()
        print("[!] Packet dropped!")
    # Accept the packet
    else:
        packet.accept()


def run_packet_manipulation():
    """The main method here, will issue a iptables command and construct the NFQUEUE"""

    try:
        # Runs the IPTABLES command
        os.system("iptables -A INPUT -j NFQUEUE")

        print("[*] Mode is: " + mode.__name__)

        # Setup for the NQUEUE
        nfqueue = NetfilterQueue()
        nfqueue.bind(0, mode)  # 0 is the default NFQUEUE

        # Shows the start waiting message
        print("[*] Waiting ")
        nfqueue.run()
    except (KeyboardInterrupt, SystemExit):
        print("\n[!] Process aborted")
        print("[!] iptables reverted")
        os.system("iptables -F")


def help_message():
    """Issues a terminal help message"""

    print("""
    Options:
    #=================================================#
    |-p                             - Print packet    |
    |-e                             - Packet edit     |
    |-l <latency_seconds>           - Latency         |
    |-pl <loss_percentage>          - Packet loss     |
    |-h                             - Help            |
    #=================================================#
    """)


def parameters():
    """This function deals with the actions attached to parameters"""

    global mode
    global latency_value_second
    global packet_loss_percentage

    # --- default vars --- #
    mode_arg = ""
    mode_value_arg = ""
    run = True
    # -------------------- #

    """Assigning Parameters"""
    # Note: The script name i.e "Python.py" is counted as a parameter
    length = len(sys.argv)
    if length == 3:
        mode_arg = str(sys.argv[1])
        mode_value_arg = str(sys.argv[2])

    elif length == 2:
        mode_arg = str(sys.argv[1])

    elif length == 1:
        print("Not enough parameters!")
        help_message()
        run = False

    """Parameter List"""
    if mode_arg == "-p":
        mode = print_packet

    elif mode_arg == "-e":
        mode = edit_packet

    elif mode_arg == "-l":
        mode = packet_latency
        latency_value_second = int(mode_value_arg) / 1000

    elif mode_arg == "-pl":
        mode = packet_loss
        packet_loss_percentage = int(mode_value_arg)

    elif mode_arg == "-h":
        help_message()
        run = False

    elif mode_arg == "-i":
        mode = ignore_packet

    #       <--- Add more parameters here

    # No parameters
    elif mode_arg == "":
        print()

    # Invalid parameters
    else:
        print("Unsupported parameters included")
        help_message()
        run = False

    # If everything is valid run == true
    if run:
        run_packet_manipulation()

# ------------------------DEFINITION END ------------------------------ #


# Default value
packet_loss_percentage = 0
latency_value_second = 0
mode = ignore_packet

# Parameter handling
parameters()
