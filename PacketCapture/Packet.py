import argparse
import signal
import threading
import textwrap
import Common_Connections
import help
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
    def t_print(packet):
        """The functionality that will spawned in a thread from the Print_Packet mode"""

        if affect_packet(packet):
            print_force("[!] " + str(packet))

        if accept:
            packet.accept()

    try:
        map_thread(t_print, [packet])
    except KeyboardInterrupt:
        clean_close()


def edit_packet(packet, accept=True):
    """This function will be used to edit sections of a packet, this is currently incomplete"""

    # Thread functionality
    def edit(packet):
        """Thread functionality"""

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
        map_thread(edit, [packet])
    except KeyboardInterrupt:
        clean_close()


def packet_latency(packet, accept=True):
    """This function is used to incur latency on packets"""

    def latency(packet):
        """Thread functionality"""

        if affect_packet(packet):
            print_force("[!] " + str(packet))

            # Issues latency of the entered value
            time.sleep(latency_value_second)

            # Accepts and lets the packet leave the queue
            if accept:
                packet.accept()

    try:
        map_thread(latency, [packet])
    except KeyboardInterrupt:
        clean_close()


def drop_packet():
    """Used so the dual packetloss-latency can use the functionality of the packet loss code"""

    # random value from 1 to 100
    random_value = random.uniform(1, 100)

    # If the generated value is smaller than the percentage discard
    if packet_loss_percentage > random_value:
        print_force("[!] Packet dropped!")

        return True
    # Accept the packet
    else:
        return False


def packet_loss(packet):
    """This function will issue a packet loss,
    a percentage is defined and anything
    lower is dropped and anything else is accepted"""

    if affect_packet(packet):
        if drop_packet():
            packet.drop()
        else:
            packet.accept()
    else:
        packet.accept()


# ISSUES
# - For some reason the value printed as 'sent' is always twice the number that actually have been sent??
# - There needs to be a wait before the packet is added to the pool?? Maybe they're being added too quickly
def throttle(packet):
    """Mode to throttle packets"""

    global throttle_pool

    # TODO: Why is this needed wait needed?
    # If the wait isn't included it will freeze the program
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
    """Event that purges the packet pool when the time has elapsed"""

    global throttle_pool, throttle_period, t_job

    # Sends all packets!
    for x in throttle_pool:
        x.accept()

    if len(throttle_pool) is not 0:
        print_force("[!] Packets sent. Number: {}".format(len(throttle_pool)))

    throttle_pool = []

    # Starts another thread
    t_job = threading.Timer(throttle_period, throttle_purge).start()


def duplicate(packet):
    """Mode that takes a full duplication"""
    global duplication_factor

    if affect_packet(packet):

        # TODO: BROKEN: Just sending the packet using scapy does not work

        pass
    else:
        packet.accept()


def packetloss_and_latency(packet):
    """This performs two of the effects together"""

    if drop_packet():
        packet.drop()
    else:
        packet_latency(packet, True)


def emulate_real_connection_speed(packet):
    global connection
    global latency_value_second, packet_loss_percentage

    latency_value_second = (connection.rnd(connection.latency) / 1000)
    packet_loss_percentage = connection.rnd(connection.packetloss)

    # Calls mode
    packetloss_and_latency(packet)


def track_bandwidth(packet):
    """This mode allows for the tracking of rate of packets recieved"""

    # Defines the potential units the rate could be measured in
    units = ['B/s', 'KB/s', 'MB/s', 'GB/s']

    global total, previous

    # Packet format
    #   '<Name> packet <Size> Bytes'
    parts = str(packet).split(' ')
    packetsize = parts[2]

    total += int(packetsize)

    # Works out rate
    now = time.time()
    elapsed = now - previous
    rate = (total / elapsed)

    # Dynamic altering of rates unit
    unit = units[0]   # Starts at 'B/s'
    times_reduced = 0

    # Increase
    while rate > 1000 and times_reduced < 3:
        rate = rate / 1000
        times_reduced += 1
        unit = units[times_reduced]

    # Decrease
    while rate < 0.1 and times_reduced > 0:
        rate = rate * 1000
        times_reduced -= 1
        unit = units[times_reduced]

    print('[*] Total: {} bytes - Rate: {:.2f} {} - Elapsed {:.2f} seconds'.format(total, rate, unit, elapsed), end='\r')
    packet.accept()

def rate_limit(packet):
    pass


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
                                     epilog=textwrap.dedent(epilog),
                                     allow_abbrev=False)

    parser.add_argument_group('Arguments',
                              description=help.Usage())

    # Mode parameters
    effect = parser.add_mutually_exclusive_group(required=True,)

    effect.add_argument('--print',
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
                        nargs=2,
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
                        help=argparse.SUPPRESS,
                        type=int)

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
        local_args = args.latency

        latency_value_second = int(local_args) / 1000
        print_force('[*] Latency set to: {}s'.format(latency_value_second))
        mode = packet_latency

    elif args.packet_loss:
        local_args = args.packet_loss

        packet_loss_percentage = int(local_args)
        print_force('[*] Packet loss set to: {}%'.format(packet_loss_percentage))
        mode = packet_loss

    elif args.throttle:
        local_args = args.throttle

        throttle_period = int(local_args) / 1000
        print_force('[*] Packet throttle delay set to {}s'.format(throttle_period))
        mode = throttle

        # Starts throttle purge thread
        t_job = threading.Timer(throttle_period, throttle_purge).start()

    elif args.duplicate:
        local_args = args.duplicate

        duplication_factor = int(local_args)
        print_force('[*] Packet duplication set. Factor is: {}'.format(duplication_factor))
        mode = duplicate

    elif args.combination:
        local_args = args.combination

        latency_value_second = int(local_args[0]) / 1000
        packet_loss_percentage = int(local_args[1])

        print_force('[*] Latency set to:        {} s'.format(latency_value_second))
        print_force('[*] Packet loss set to:    {} %'.format(packet_loss_percentage))

        mode = packetloss_and_latency

    elif args.simulate:
        local_args = args.simulate

        global connection

        connection = None
        for c in Common_Connections.connections:
            if c.name == str(local_args):
                connection = c

        # Could not find connection type
        if connection is None:
            print('Error: Could no find the \'{}\' connection entered'.format(local_args))
            sys.exit(0)

        print_force('[*] Connection type is emulating: {}'.format(connection.name))

        mode = emulate_real_connection_speed

    elif args.display_bandwidth:
        global total, previous
        total = 0
        previous = time.time()
        mode = track_bandwidth

    # Extra settings
    if args.target_packet:
        local_args = args.target_packet

        target_packet_type = local_args
        print_force('[!] Only affecting {} packets'.format(target_packet_type))

    if args.arp:
        local_args = args.arp

        print_force("[!] Arp spoofing mode activated")
        arp_active = True
        victim_ip = local_args[0]
        router_ip = local_args[1]
        interface = local_args[2]

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
