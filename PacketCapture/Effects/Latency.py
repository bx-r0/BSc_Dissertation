import time


class Latency:

    def __init__(self, latency_value, accept, method_print):
        self.accept = accept
        self.latency_value = latency_value / 1000
        self.method_print = method_print
        self._print('[*] Latency set to: {}s'.format(self.latency_value), force=True)

        # Stats
        self.total_packets = 0

    def _print(self, message, end='\n', force=False):
        if self.method_print or force:
            print(message, flush=True, end=end)

    def print_stats(self):
        self._print('[*] Total Packets effected: {}'.format(self.total_packets), end='\r')

    def effect(self, packet):
        """Thread functionality"""

        self.print_stats()
        self.total_packets += 1

        # Issues latency of the entered value
        time.sleep(self.latency_value)

        # Accepts and lets the packet leave the queue
        if self.accept:
            packet.accept()

    def alter_latency_value(self, new_value):
        """This is useful if latency isn't static and can be obtained from a range"""
        self._print('[*] Latency: {:.2f}s - '.format(new_value), end='')
        self.latency_value = new_value

