import time


class Bandwidth:
    """Class that deals with bandwidth functionality"""
    def __init__(self, bandwidth=0):
        self.units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        self.total = 0
        self.rate = 0
        self.unit = self.units[0]
        self.startTime = time.time()
        self.packet_backlog = []

        self.bandwidth = bandwidth
        if bandwidth is not 0:
            print('[*] Bandwidth set to: {} B/s'.format(bandwidth))

    def calculate_rate(self):
        """Calculates the rate of throughput"""

        # Works out rate
        now = time.time()
        self.rate = (self.total / (now - self.startTime))

    @staticmethod
    def calculate_packet_size(packet_name):
        """Grabs the size of the packet from the name of the packet"""

        # Packet format
        #   '<Name> packet <Size> Bytes'
        parts = str(packet_name).split(' ')
        packet_size = parts[2]
        return int(packet_size)

    def recalculate_units(self, rate):
        """Recalculates the units when they flow over.
        For example KBs -> MBs """

        times_reduced = 0

        # Dynamic altering of rates unit
        self.unit = self.units[0]  # Starts at 'B/s'

        # Increase
        while rate > 1000 and times_reduced < 3:
            rate = rate / 1000
            times_reduced += 1
            self.unit = self.units[times_reduced]

        # Decrease
        while rate < 0.1 and times_reduced > 0:
            rate = rate * 1000
            times_reduced -= 1
            self.unit = self.units[times_reduced]

        return rate

    def print_stats(self):
        print('[*] Total: {} bytes - Rate: {:.2f} {} '.format(self.total, self.rate, self.unit), end='\r')

    def display(self, packet):
        """Used to display the bandwidth"""

        # Updates the total
        self.total += self.calculate_packet_size(packet)

        # Deals with the rate calculation
        self.calculate_rate()

        self.rate = self.recalculate_units(self.rate)

        self.print_stats()

    def send_packet(self, packet):
        """Sends a packet and increases the total"""

        self.total += self.calculate_packet_size(packet)
        packet.accept()
        self.calculate_rate()

    def limit(self, packet):
        """Used to limit the bandwidth of the channel"""

        # Refresh
        self.print_stats()
        self.calculate_rate()

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
