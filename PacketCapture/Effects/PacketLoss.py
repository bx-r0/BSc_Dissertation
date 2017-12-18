import random


# TODO: Add print parameter to this module
class PacketLoss:

    def __init__(self, percentage, accept=True, method_print=True):
        self.packet_loss_percentage = int(percentage)
        self.accept = accept
        self.method_print = method_print
        self._print('[*] Packet loss set to: {}%'.format(percentage), force=True)

        # Stats
        self.total_packets = 0
        self.dropped_packets = 0

    def _print(self, message, end='\n', force=False):
        if self.method_print or force:
            print(message, end=end, flush=True)

    def print_stats(self):
        if not self.total_packets == 0:
            dropped_percentage = (self.dropped_packets / self.total_packets) * 100
        else:
            dropped_percentage = 0

        self._print("[*] Total Packets: {} - Average Loss {:.2f}%".
                    format(self.total_packets, dropped_percentage), end='\r')

    def effect(self, packet):
        """This function will issue packet loss,
           a percentage is defined and anything
           lower is dropped and anything higher is accepted"""

        # random value from 0 to 100
        random_value = random.uniform(0, 100)

        self.total_packets += 1

        # If the generated value is smaller than the percentage discard
        if self.packet_loss_percentage > random_value:
            self.dropped_packets += 1
            packet.drop()

        # Accept the packet
        else:
            if self.accept:
                packet.accept()

        self.print_stats()

    def alter_percentage(self, new_value):
        self._print('Packet loss: {}% -- '.format(new_value), end='')
        self.packet_loss_percentage = new_value
