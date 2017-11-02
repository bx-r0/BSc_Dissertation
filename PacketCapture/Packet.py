from scapy.all import *
from netfilterqueue import NetfilterQueue

"""
This iptables command needs to be run to push all packets into the NFQUEUE:

        "sudo iptables -A INPUT -j NFQUEUE"

To restore full internet connection run:

        "sudo iptables -F"
"""


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


def run_packet_manipulation():
    try:
        # Runs the IPTABLES command
        os.system("iptables -A INPUT -j NFQUEUE")

        # Setup for the NQUEUE
        nfqueue = NetfilterQueue()
        nfqueue.bind(0, mode)  # 0 is the default NFQUEUE

        # Prints the mode the program is running in
        print("[*] Mode is: ", end='')
        print(mode.__name__)

        # Shows the start waiting message
        print("[*] Waiting ")
        nfqueue.run()

        # Clears the set IPTABLES rule
        os.system("iptables -F")

    except KeyboardInterrupt:
        pass


"""
Parameter format:
                  (0)      (1)         (2)
    sudo python Packet.py <mode> <value_for_mode>
    
"""
# Assigns parameter values
mode_arg = str(sys.argv[1])
if len(sys.argv) > 2:
    mode_value_arg = str(sys.argv[2])
else:
    raise Exception("Not enough parameters passed when calling Packet.py")

# ------SWITCH CASE FOR PARAMETERS PASSED -----#
if mode_arg == "-p":
    mode = print_packet

elif mode_arg == "-e":
    mode = edit_packet

elif mode_arg == "-l":
    mode = packet_latency
    latency_value_second = mode_value_arg

elif mode_arg == "-pl":
    mode = packet_loss
    packet_loss_percentage = mode_value_arg
# ----------------------------------------------#

# -------VARIABLES---------- #
mode = print_packet  # <-- Change this variable to change the network degradation type

# Degradation characteristic
packet_loss_percentage = 10
latency_value_second = 1
# -------------------------- #

run_packet_manipulation()
