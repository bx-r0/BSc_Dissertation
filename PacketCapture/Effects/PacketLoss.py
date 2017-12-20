from Effects.Effect import Effect
import random


class PacketLoss(Effect):

    def __init__(self, percentage, accept_packets=True, show_output=True):
        super().__init__(accept_packets, show_output)

        self.packet_loss_percentage = int(percentage)
        self.print('[*] Packet loss set to: {}%'.format(percentage), force=True)

        # Stats
        self.total_packets = 0
        self.dropped_packets = 0

    def print_stats(self):
        if not self.total_packets == 0:
            dropped_percentage = (self.dropped_packets / self.total_packets) * 100
        else:
            dropped_percentage = 0

        self.print("[*] Total Packets: {} - Average Loss {:.2f}%".format(
            self.total_packets, dropped_percentage), end='\r')

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
            self.accept(packet)

        self.print_stats()

    def alter_percentage(self, new_value):
        self.print('Packet loss: {}% -- '.format(new_value), end='')
        self.packet_loss_percentage = new_value
