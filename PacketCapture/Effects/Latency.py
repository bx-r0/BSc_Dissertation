import time


class Latency:

    def __init__(self, latency_value, accept):
        self.accept = accept
        self.latency_value = latency_value / 1000
        print('[*] Latency set to: {}s'.format(self.latency_value), flush=True)

    def effect(self, packet):
        """Thread functionality"""

        print("[!]", str(packet), flush=True)

        # Issues latency of the entered value
        time.sleep(self.latency_value)

        # Accepts and lets the packet leave the queue
        if self.accept:
            packet.accept()

    def alter_latency_value(self, new_value):
        """This is useful if latency isn't static and can be obtained from a range"""
        print('[*] Latency: {:.2f}s - '.format(new_value), flush=True, end='')
        self.latency_value = new_value

