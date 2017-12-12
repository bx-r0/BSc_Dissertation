import argparse
import signal
import threading
import textwrap
from netfilterqueue import NetfilterQueue
from scapy.all import *
from multiprocessing.dummy import Pool as ThreadPool

# Defines how many threads are in the pool
pool = ThreadPool(100)

# Formatting messages for the usage
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
        pool.map(method, args)
    except ValueError:
        # Stops the program from exploding when he pool is terminated
        pass


def print_force(str):
    """This method is required because when this python file is called as a script
    the prints don't appear and a flush is required """
    print(str, flush=True)


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


def print_packet(packet, accept=True):
    """This function just prints the packet"""

    # Thread functionality
    def _print_thread(packet):
        """The functionality that will spawned in a thread from the Print_Packet mode"""

        if affect_packet(packet):
            print_force("[!] " + str(packet))

        if accept:
            packet.accept()

    try:
        map_thread(_print_thread, [packet])
    except KeyboardInterrupt:
        clean_close()


def edit_packet(packet, accept=True):
    """This function will be used to edit sections of a packet, this is currently incomplete"""

    # Thread functionality
    def _edit_thread(packet):

        if affect_packet(packet):
            pkt = IP(packet.get_payload())

            # Changes the Time To Live of the packet
            pkt.ttl = 150

            # Recalculates the check sum
            del pkt[IP].chksum

            # Sets the packet to the modified version
            packet.set_payload(bytes(pkt))

            if accept:
                packet.accept()
        else:
            packet.accept()

    try:
        map_thread(_edit_thread, [packet])
    except KeyboardInterrupt:
        clean_close()


def packet_latency(packet, accept=True):
    """This function is used to incur latency on packets"""

    # Thread functionality
    def _latency_thread(packet):

        if affect_packet(packet):
            print_force("[!] " + str(packet))

            # Issues latency of the entered value
            time.sleep(latency_value_second)

            # Accepts and lets the packet leave the queue
            if accept:
                packet.accept()

    try:
        map_thread(_latency_thread, [packet])
    except KeyboardInterrupt:
        clean_close()


def packet_loss(packet, accept=True):
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
            if accept:
                packet.accept()
    # This else is needed because the packet would be blocked if it's not the target
    else:
        packet.accept()

# ISSUES
# - For some reason the value printed as 'sent' is always twice the number that actually have been sent??
# - There needs to be a wait before the packet is added to the pool?? Maybe they're being added too quickly


def throttle(packet):
    """Mode to throttle packets"""

    global throttle_pool

    # TODO: Why is this needed?
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    if affect_packet(packet):
        # Adds the packet to the pool
        throttle_pool.append(packet)
    else:
        packet.accept()


def throttle_purge():
    """Event that purges the packet pool"""

    global throttle_pool, throttle_period, t_job

    # Sends all packets!
    for x in throttle_pool:
        x.accept()

    if len(throttle_pool) is not 0:
        print_force("[!] Packets sent. Number: {}".format(len(throttle_pool)))

    throttle_pool = []

    # Starts another thread
    t_job = threading.Timer(throttle_period, throttle_purge).start()


def duplicate(packet, accept=True):
    """Mode that takes a full duplication"""
    global duplication_factor

    if affect_packet(packet):

        # TODO: BROKEN: Just sending the packet using scapy does not work

        pass
    else:
        packet.accept()


def run_packet_manipulation():
    """The main method here, will issue a iptables command and construct the NFQUEUE"""

    try:
        global nfqueue
        global arp_process

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

        # Runs the arp spoofing
        if arp_active:
            arp_spoof_external(interface, routerIP, victimIP)

        # Shows the start waiting message
        print_force("[*] Waiting ")
        nfqueue.run()

    except KeyboardInterrupt:
        clean_close()


def parameters():
    """This function deals with parameters passed to the script
    most of the handling is performed by the 'getopt' module"""

    # Defines globals to be used above
    global mode, latency_value_second, packet_loss_percentage, target_packet_type, duplication_factor
    global victim_ip, router_ip, interface, arp_active
    global throttle_period, throttle_pool, t_job

    # Defaults
    mode = print_packet
    target_packet_type = 'ALL'
    arp_active = False
    throttle_pool = []
    t_job = None

    # Arguments
    parser = argparse.ArgumentParser(prog="Packet.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(logo),
                                     epilog=textwrap.dedent(epilog))

    # Mode parameters
    effect = parser.add_mutually_exclusive_group(required=False)
    effect.add_argument('-p', '--print',
                        action='store_true',
                        help='Sets the mode to print_packet')

    effect.add_argument('-l',
                        action='store',
                        help='Latency - Sets the mode to packet_latency (ms)',
                        metavar='<delay>')

    effect.add_argument('-z',
                        action='store',
                        help='Packet_Loss - Sets the mode to packet_loss (percentage)',
                        metavar='<loss_percent>')

    effect.add_argument('-d',
                        action='store',
                        help='Throttle - Specifies a length of time to hold all packets and release in one go (ms)',
                        metavar='<delay>')

    effect.add_argument('-m',
                        action='store',
                        help='Specifies the duplication factor',
                        metavar='<factor>')

    effect.add_argument('-c',
                        action='store',
                        nargs=2,
                        help='Specifies to use Latency and Packet loss together',
                        metavar=('<latency>', '<packet_loss>'))

    # Extra parameters
    parser.add_argument('-t',
                        action='store',
                        help="Specifies a packet type to affect",
                        metavar='<packet_protocol>')

    parser.add_argument('-a',
                        action='store',
                        nargs=3,
                        help="Specifies values for arp spoofing mode",
                        metavar=('<victimIP>', '<routerIP>', '<interface>'))

    args = parser.parse_args()

    # Modes
    if args.print:
        mode = print_packet

    elif args.l:
        latency_value_second = int(args.l) / 1000
        print_force('[*] Latency set to: {}ms'.format(latency_value_second))
        mode = packet_latency

    elif args.z:
        packet_loss_percentage = int(args.z)
        print_force('[*] Packet loss set to: {}%'.format(packet_loss_percentage))
        mode = packet_loss

    elif args.d:
        throttle_period = int(args.d) / 1000
        print_force('[*] Packet throttle delay set to {}ms'.format(throttle_period))
        mode = throttle

        # Starts throttle purge thread
        t_job = threading.Timer(throttle_period, throttle_purge).start()

    elif args.m:
        duplication_factor = int(args.m)
        print_force('[*] Packet duplication set. Factor is: {}'.format(duplication_factor))
        mode = duplicate

    elif args.c:
        latency_value_second = int(args.c[0])
        packet_loss_percentage = int(args.c[1])

        print_force('[*] Latency set to:        {} ms'.format(latency_value_second))
        print_force('[*] Packet loss set to:    {} %'.format(packet_loss_percentage))

        # TODO: Add a multi method? Maybe something that incorperates both effects
        #mode = [packet_latency, packet_loss]

    # Extra settings
    if args.t:
        target_packet_type = args.t
        print_force('[!] Only affecting {} packets'.format(target_packet_type))

    if args.a:
        print_force("[!] Arp spoofing mode activated")
        arp_active = True
        victim_ip = args.arp[0]
        router_ip = args.arp[1]
        interface = args.arp[2]

    # When all parameters are handled
    run_packet_manipulation()


def kill_thread_pool():
    # Death to the thread pool
    pool.close()
    print_force("\n[!] Thread pool killed")


def clean_close(signum='', frame=''):
    """Used to close the script cleanly"""

    global t_job

    if t_job is not None:
        t_job.terminate()

    stop_pool = threading.Thread(target=kill_thread_pool)
    stop_pool.start()

    if arp_active:
        arp_process.send_signal(signal.SIGINT)

    print_force("[!] iptables reverted")
    os.system("iptables -F INPUT")

    print_force("[!] NFQUEUE unbinded")
    nfqueue.unbind()
    os._exit(0)


# Rebinds the all the close signals to clean_close the script
signal.signal(signal.SIGTSTP, clean_close)  # Ctrl+Z
signal.signal(signal.SIGQUIT, clean_close)  # Ctrl+\

# Check if user is root
if os.getuid() != 0:
    exit("Error: User needs to be root to run this script")

parameters()
