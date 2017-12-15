import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Suppresses the Scapy WARNING Message

import argparse
import signal
import threading
import textwrap
import Common_Connections
import help

# From Imports
from netfilterqueue import NetfilterQueue
from scapy.all import *
from multiprocessing.dummy import Pool as ThreadPool

# Effect imports
from Effects.Latency import Latency
from Effects.LimitBandwidth import Bandwidth
from Effects.PacketLoss import PacketLoss
from Effects.Throttle import Throttle
from Effects.OutOfOrder import Order

# Defines how many threads are in the pool
pool = ThreadPool(2000)

logo = """
==============================================================
Degraded Packet Simulation

    ██████╗ ██████╗ ███████╗
    ██╔══██╗██╔══██╗██╔════╝
    ██║  ██║██████╔╝███████╗
    ██║  ██║██╔═══╝ ╚════██║
    ██████╔╝██║     ███████║
    ╚═════╝ ╚═╝     ╚══════╝
"""

epilog = """
Aidan Fray
afray@hotmail.co.uk

==============================================================
"""


def map_thread(method, args):
    """Method that deals with the threading of the packet manipulation"""

    # If this try is caught, it occurs for every thread active so anything in the
    # except is triggered for all active threads
    try:
        pool.map_async(method, args)
    except ValueError:
        # Stops the program from exploding when he pool is terminated
        pass


def print_force(message):
    """This method is required because when this python file is called as a script
    the prints don't appear and a flush is required """
    print(message, flush=True)


def affect_packet(packet):
    """This function checks if the packet should be affected or not. This is part of the -t option"""

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


def print_packet(packet, accept=True):
    """This function just prints the packet"""

    # Thread functionality
    def t_print(t_packet):
        """The functionality that will spawned in a thread from the Print_Packet mode"""

        if affect_packet(t_packet):
            print_force("[!] " + str(t_packet))

        if accept:
            t_packet.accept()

    map_thread(t_print, [packet])


def edit_packet(packet, accept=True):
    """This function will be used to edit sections of a packet, this is currently incomplete"""

    # Thread functionality
    def edit(t_packet):
        """Thread functionality"""

        if affect_packet(t_packet):
            pkt = IP(t_packet.get_payload())

            # Changes the Time To Live of the packet
            pkt.ttl = 150

            # Recalculates the check sum
            del pkt[IP].chksum

            # Sets the packet to the modified version
            t_packet.set_payload(bytes(pkt))

            if accept:
                t_packet.accept()
        else:
            t_packet.accept()

    try:
        map_thread(edit, [packet])
    except KeyboardInterrupt:
        clean_close()


def packet_latency(packet):
    """This function is used to incur latency on packets"""
    if affect_packet(packet):
        map_thread(latency_obj.effect, [packet])
    else:
        packet.accept()


def packet_loss(packet):
    """Function that performs packet loss on all packets"""
    if affect_packet(packet):
        map_thread(packet_loss_obj.effect, [packet])
    else:
        packet.accept()


def throttle(packet):
    """Mode assigned to throttle packets"""
    if affect_packet(packet):
        throttle_obj.effect(packet)
    else:
        packet.accept()


def duplicate(packet):
    """Mode that takes a full duplication"""
    global duplication_factor
    if affect_packet(packet):
        # TODO: BROKEN: Just sending the packet using scapy does not work
        pass
    else:
        packet.accept()


def combination(packet):
    """This performs two of the effects together"""
    packet_loss_obj.effect(packet)
    latency_obj.effect(packet)
    bandwidth_obj.limit(packet)


def emulate_real_connection_speed(packet):
    """Used to emulate real world connections speeds"""
    global connection

    if affect_packet(packet):

        # Adjusts the values
        latency_obj.alter_latency_value(connection.rnd_latency())
        packet_loss_obj.alter_percentage(connection.rnd_packet_loss())
        bandwidth_obj.alter_bandwith(connection.rnd_bandwidth())

        # Calls mode
        combination(packet)
    else:
        packet.accept()


def track_bandwidth(packet):
    """This mode allows for the tracking of rate of packets recieved"""
    if affect_packet(packet):
        bandwidth_obj.display(packet)
    else:
        packet.accept()


def limit_bandwidth(packet):
    """This is mode for limiting the rate of transfer"""
    if affect_packet(packet):
        bandwidth_obj.limit(packet)
    else:
        packet.accept()


def out_of_order(packet):
    """Mode that alters the order of packets"""
    if affect_packet(packet):
        order_obj.effect(packet)
    else:
        packet.accept()


def run_packet_manipulation():
    """The main method here, will issue a iptables command and construct the NFQUEUE"""

    try:
        global nfqueue

        # Packets for this machine
        os.system("iptables -A INPUT -j NFQUEUE")

        # Packets for forwarding or other routes
        os.system("iptables -t nat -A PREROUTING -j NFQUEUE")

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

    except KeyboardInterrupt:
        clean_close()


def parameters():
    """This function deals with parameters passed to the script"""

    # Defines globals to be used above
    global mode, target_packet_type, duplication_factor, arp_active

    global latency_obj, throttle_obj, packet_loss_obj, bandwidth_obj, order_obj
    latency_obj = None
    throttle_obj = None
    packet_loss_obj = None
    bandwidth_obj = None
    order_obj = None

    # Defaults
    mode = print_packet
    target_packet_type = 'ALL'
    arp_active = False

    # Arguments
    parser = argparse.ArgumentParser(prog="Packet.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(logo),
                                     epilog=textwrap.dedent(epilog),
                                     allow_abbrev=False)

    parser.add_argument_group('Arguments', description=help.Usage())

    # Mode parameters
    effect = parser.add_mutually_exclusive_group(required=True,)

    effect.add_argument('--print', '-p',
                        action='store_true',
                        help=argparse.SUPPRESS)

    effect.add_argument('--latency', '-l',
                        action='store',
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--packet-loss', '-pl',
                        action='store',
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--throttle', '-t',
                        action='store',
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--duplicate', '-d',
                        action='store',
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--combination', '-c',
                        action='store',
                        nargs=3,
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--simulate', '-s',
                        action='store',
                        help=argparse.SUPPRESS)

    effect.add_argument('--display-bandwidth', '-b',
                        action='store_true',
                        help=argparse.SUPPRESS)

    effect.add_argument('--rate-limit', '-rl',
                        action='store',
                        dest='rate_limit',
                        help=argparse.SUPPRESS,
                        type=int)

    effect.add_argument('--out-of-order', '-o',
                        action='store_true',
                        dest='order',
                        help=argparse.SUPPRESS)

    # Extra parameters
    parser.add_argument('--target-packet', '-tp',
                        action='store',
                        help=argparse.SUPPRESS)

    parser.add_argument('--arp', '-a',
                        action='store',
                        nargs=3,
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Modes
    if args.print:
        mode = print_packet

    elif args.latency:
        latency_obj = Latency(latency_value=args.latency, accept=True)
        mode = packet_latency

    elif args.packet_loss:
        packet_loss_obj = PacketLoss(percentage=args.packet_loss, accept=True)
        mode = packet_loss

    elif args.throttle:
        throttle_obj = Throttle(period=args.throttle)
        throttle_obj.start_purge_monitor()
        mode = throttle

    elif args.duplicate:
        local_args = args.duplicate

        duplication_factor = int(local_args)
        print_force('[*] Packet duplication set. Factor is: {}'.format(duplication_factor))
        mode = duplicate

    elif args.combination:
        latency_obj = Latency(latency_value=args.combination[0], accept=False)
        bandwidth_obj = Bandwidth(bandwidth=args.combination[2], accept=False, print_f=False)
        packet_loss_obj = PacketLoss(percentage=args.combination[1], accept=True)
        mode = combination

    elif args.simulate:
        global connection

        # Checks if the parameter is a valid connection
        connection = None
        for c in Common_Connections.connections:
            if c.name == str(args.simulate):
                connection = c
        # Could not find connection type
        if connection is None:
            print('Error: Could no find the \'{}\' connection entered'.format(args.simulate))
            sys.exit(0)

        print_force('[*] Connection type is emulating: {}'.format(connection.name))

        latency_obj = Latency(latency_value=0, accept=False)
        packet_loss_obj = PacketLoss(percentage=0, accept=False)
        bandwidth_obj = Bandwidth(bandwidth=0, accept=True)
        mode = emulate_real_connection_speed

    elif args.display_bandwidth:
        bandwidth_obj = Bandwidth()
        mode = track_bandwidth

    elif args.rate_limit:
        # Sets the bandwidth object with the specified bandwidth limit
        bandwidth_obj = Bandwidth(args.rate_limit)
        mode = limit_bandwidth

    elif args.order:
        order_obj = Order()
        mode = out_of_order

    # Extra settings
    if args.target_packet:
        local_args = args.target_packet

        target_packet_type = local_args
        print_force('[!] Only affecting {} packets'.format(target_packet_type))

    if args.arp:
        global arp_process

        local_args = args.arp

        print_force("[*] ## ARP spoofing mode activated ## ")

        victim = local_args[0]
        router = local_args[1]
        interface = local_args[2]

        filepath = os.path.dirname(os.path.abspath(__file__))

        # Runs the arp spoofing
        arp_active = True
        cmd = ['pkexec', 'python', filepath + '/ArpSpoofing.py']
        cmd = cmd + ['-t', victim, '-r', router, '-i', interface]
        arp_process = subprocess.Popen(cmd)

    # When all parameters are handled
    run_packet_manipulation()


def kill_thread_pool():
    # Death to the thread pool
    pool.close()
    print_force("[!] Thread pool killed\n")


def stop_object(object):
    try:
        object.stop()
    except NameError:
        pass


def clean_close(signum='', frame=''):
    """Used to close the script cleanly"""

    # Kills any threads running in objects
    stop_object(throttle_obj)
    stop_object(order_obj)

    print_force("\n[*] ## Close signal recieved ##")

    # Resets
    print_force("[!] iptables reverted")
    os.system("iptables -F INPUT")

    print_force("[!] NFQUEUE unbinded")
    nfqueue.unbind()

    if arp_active:
        print_force('[!] Arp Spoofing stopped!')
        arp_process.terminate()

    # Kills thread pool
    stop_pool = threading.Thread(target=kill_thread_pool)
    stop_pool.start()

    os._exit(0)


# Rebinds the all the close signals to clean_close the script
signal.signal(signal.SIGINT, clean_close)   # Ctrl + C
signal.signal(signal.SIGTSTP, clean_close)  # Ctrl + Z
signal.signal(signal.SIGQUIT, clean_close)  # Ctrl + \

# Check if user is root
if os.getuid() != 0:
    exit("Error: User needs to be root to run this script")

parameters()
