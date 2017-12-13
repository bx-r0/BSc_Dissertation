import time


class Bandwidth:
    """Class that deals with bandwidth functionality"""
    def __init__(self):
        self.units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        self.total = 0
        self.rate = 0
        self.unit = self.units[0]
        self.startTime = time.time()

    @staticmethod
    def calculate_rate(total, previous):
        """Calculates the rate of throughput"""

        # Works out rate
        now = time.time()
        rate = (total / (now - previous))
        return rate

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

    def display(self, packet):
        """Used to display the bandwidth"""

        # Updates the total
        self.total += self.calculate_packet_size(packet)

        # Deals with the rate calculation
        rate = self.calculate_rate(self.total, self.startTime)
        rate = self.recalculate_units(rate)

        print('[*] Total: {} bytes - Rate: {:.2f} {} '.format(self.total, rate, self.unit), end='\r')

    def limit(self, packet):
        # TODO
        pass

