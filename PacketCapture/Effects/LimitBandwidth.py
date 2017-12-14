import time
import threading
import os

# Grabs terminals size
height, width = os.popen('stty size').read().split(' ')


class Bandwidth:
    """Class that deals with bandwidth functionality"""
    def __init__(self, bandwidth=0):
        self.units = ['B', 'KB', 'MB', 'GB']

        self.total = 0
        self.transferred_since_check = 0
        self.rate = 0

        self.previous = time.time()
        self.start = time.time()

        self.packet_backlog = []

        # Variable that defines how often the stats are updated
        self.rate_update_period = 1 # In seconds

        self.bandwidth = bandwidth
        if bandwidth is not 0:
            print('[*] Bandwidth set to: {} B/s'.format(bandwidth))

        self.start_rate_update()

    def calculate_rate(self):
        """Calculates the rate of throughput"""

        # Const variable that is the period of time the rate is calculated over
        # Measured in seconds

        now = time.time()
        elapsed = (now - self.previous)

        # Refresh rate
        if elapsed > self.rate_update_period:
            self.rate = (self.transferred_since_check / elapsed)
            self.print_stats()

            # Reset
            self.transferred_since_check = 0
            self.previous = now

        self.start_rate_update()

    @staticmethod
    def calculate_packet_size(packet_name):
        """Grabs the size of the packet from the name of the packet"""

        # Packet format
        #   '<Name> packet <Size> Bytes'
        parts = str(packet_name).split(' ')
        packet_size = parts[-2]
        return int(packet_size)

    def recalculate_units(self, value):
        """Recalculates the units when they flow over.
        For example KBs -> MBs """

        times_reduced = 0
        unit = self.units[times_reduced]

        # Increase
        while value > 1000 and times_reduced < 3:
            value = value / 1000
            times_reduced += 1
            unit = self.units[times_reduced]

        # Decrease
        while value < 0.1 and times_reduced > 0:
            value = value * 1000
            times_reduced -= 1
            unit = self.units[times_reduced]

        return value, unit

    def print_stats(self):

        # Displays totals and rate in more relevant units
        print_rate, unit_rate = self.recalculate_units(self.rate)
        print_total, unit_total = self.recalculate_units(self.total)

        # This line justs makes sure there is sections of previous lines present
        print(' ' * int(width), end='\r')
        print('[*] Total: {:.1f} {} - Rate: {:.1f} {}/s '.format(print_total, unit_total, print_rate, unit_rate), end='\r')

    def display(self, packet):
        """Used to display the bandwidth"""

        packet_size = self.calculate_packet_size(packet)

        # Updates the total
        self.total += packet_size
        self.transferred_since_check += packet_size

    def send_packet(self, packet):
        """Sends a packet and increases the total"""
        packet_size = self.calculate_packet_size(packet)

        self.total += packet_size
        self.transferred_since_check += packet_size

        packet.accept()

    def limit(self, packet):
        """Used to limit the bandwidth of the channel"""

        # Check if rate is over
        if self.rate > self.bandwidth:
            self.packet_backlog.append(packet)

        # If it's not over, send packets until it is over
        else:
            self.send_packet(packet)

            while self.rate < self.bandwidth and len(self.packet_backlog) > 0:
                self.send_packet(self.packet_backlog[0])

                # Packet is removed from the list
                del self.packet_backlog[0]

    def start_rate_update(self):
        threading.Timer(self.rate_update_period, self.calculate_rate).start()
