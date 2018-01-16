from Effects.Effect import Effect
import time


class Latency(Effect):

    def __init__(self, latency_value, accept_packets=True, show_output=True, graphing=False):
        super().__init__(accept_packets, show_output, graphing)

        self.latency_value = latency_value / 1000
        self.print('[*] Latency set to: {}s'.format(self.latency_value), force=True)
        self.total_packets = 0

    def print_stats(self):
        self.print('[*] Total Packets effected: {}'.format(self.total_packets), end='\r')

    def effect(self, packet):
        """Thread functionality"""

        # Turning the graphing mode on
        if self.graphing:
            self.graphing_effect(packet)

        self.print_stats()
        self.total_packets += 1

        # Issues latency of the entered value
        time.sleep(self.latency_value)

        self.accept(packet)

    def graphing_effect(self, packet):
        """Performs the data collectiong for the graph"""

        # Graph that tracks types of packets in the session
        sections = str(packet).split(' ')
        self.graph.increment_catagory(sections[0])

    def alter_latency_value(self, new_value):
        """This is useful if latency isn't static and can be obtained from a range"""
        self.print('[*] Latency: {:.2f}s - '.format(new_value), end='')
        self.latency_value = new_value

    def stop(self):
        self.graph.bar()
