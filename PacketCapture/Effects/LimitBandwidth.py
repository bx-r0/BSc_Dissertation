from Effects.Effect import Effect
import time
import threading
import os


class Bandwidth(Effect):
    """
    Class that deals with bandwidth functionality
    - Bandwidth (rate limiting)
    - Displaying Bandwidth
    """

    def __init__(self, bandwidth=0, accept_packets=True, show_output=True, graphing=False, graph_type_num=0):
        super().__init__(accept_packets, show_output, graphing, graph_type_num)

        # Constants
        self.units = ['B', 'KB', 'MB', 'GB']

        # General variables
        self.total = 0
        self.transferred_since_check = 0
        self.rate = 0
        self.packet_backlog = []

        # Time variables
        self.previous = time.time()
        self.start = time.time()

        # # CHARACTERISTICS # #
        # Can be changed
        self.rate_update_period = 1  # In seconds

        self.bandwidth = bandwidth
        if bandwidth is not 0:
            self.print('[*] Bandwidth set to: {} B/s'.format(bandwidth), force=True)

        self.start_rate_update()

    # -b Option
    def display(self, packet):
        """Used to display the bandwidth"""

        self.default_graphing(packet)
        self.send_packet(packet)

    # -rl Option
    def limit(self, packet):
        """Used to limit the bandwidth rate"""

        self.default_graphing(packet)

        # Check if rate is over the limit
        if self.rate > self.bandwidth:
            self.packet_backlog.append(packet)

        # If it's not over, send packets until it is over
        else:
            self.send_packet(packet)

            while self.rate < self.bandwidth and len(self.packet_backlog) > 0:
                self.send_packet(self.packet_backlog[0])

                self.calculate_rate()

                # Packet is removed from the list
                del self.packet_backlog[0]

    def print_stats(self):
        """Stat output"""

        # Displays totals and rate in more relevant units
        print_rate, unit_rate = self.recalculate_units(self.rate)
        print_total, unit_total = self.recalculate_units(self.total)

        # This line justs makes sure there is sections of previous lines present
        self.print('[*] Total: {:.1f} {} - Rate: {:.1f} {}/s '.format(
            print_total, unit_total, print_rate, unit_rate), end='\r')

    def calculate_rate_job(self):
        """Calculates the rate of throughput"""
        self.calculate_rate()
        self.start_rate_update()

    def calculate_rate(self):
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

    def send_packet(self, packet):
        """Sends a packet and increases the total"""
        packet_size = self.calculate_packet_size(packet)

        self.total += packet_size
        self.transferred_since_check += packet_size

        self.accept(packet)


    def start_rate_update(self):
        """Used to start the thread that updates the rate of transfer"""
        threading.Timer(self.rate_update_period, self.calculate_rate_job).start()

    def alter_bandwidth(self, new_value):
        """Used to change bandwidth variable for an outside location"""
        self.bandwidth = new_value

    """Graphing methods"""
    def graphing_setup(self):
        # Graph with Rate x Time
        if self.graph_type_num is 1:
            self.graph.set_x_axis_label('Time (s)')
            self.graph.set_y_axis_label('Rate (B/s)')

    def graphing_effect(self, packet):
        if self.graph_type_num is 1:
            self.graph.add_points(self.get_elapsed_time(), self.rate)

    def show_graph(self):
        # Graph with Rate x Time
        if self.graph_type_num is 1:
            self.graph.plot('r,-')
