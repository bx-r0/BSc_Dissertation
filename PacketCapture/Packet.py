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

    # Issues latency of the entered value
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

        # Shows the start waiting message
        print("[*] Waiting ")
        nfqueue.run()

    except KeyboardInterrupt:
        pass


def help_message():
    print(
        """
        Options:
        #=================================================#
        |-p                             - Print packet    |
        |-e                             - Packet edit     |
        |-l <latency_seconds>           - Latency         |
        |-pl <loss_percentage>          - Packet loss     |
        |-h                             - Help            |
        #=================================================#
        """)


"""
Parameter format:
                  (0)      (1)         (2)
    sudo python Packet.py <mode> <value_for_mode>
    
"""
# Assigns parameter values
mode_arg = str(sys.argv[1])
if len(sys.argv) > 2:
    mode_value_arg = str(sys.argv[2])

# ------SWITCH CASE FOR PARAMETERS PASSED -----#
# Print packet
if mode_arg == "-p":
    mode = print_packet
# Edit packet
elif mode_arg == "-e":
    mode = edit_packet
# Latency
elif mode_arg == "-l":
    mode = packet_latency
    latency_value_second = int(mode_value_arg) / 1000
# Packet Loss
elif mode_arg == "-pl":
    mode = packet_loss
    packet_loss_percentage = int(mode_value_arg)
# Help
elif mode_arg == "-h":
    help_message()
# Default
else:
    mode = print_packet
# ----------------------------------------------#
run_packet_manipulation()
