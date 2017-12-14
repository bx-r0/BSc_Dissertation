import random


class PacketLoss:

    def __init__(self, percentage, accept):
        self.packet_loss_percentage = int(percentage)
        self.accept = accept
        print('[*] Packet loss set to: {}%'.format(percentage), flush=True)

        # Stats
        self.total_packets = 0
        self.dropped_packets = 0

    def print_stats(self):
        if not self.total_packets == 0:
            dropped_percentage = (self.dropped_packets / self.total_packets) * 100
        else:
            dropped_percentage = 0

        # TODO: Dynamic terminal width
        print(' ' * 20, end='\r')
        print("[*] Total Packets: {} - Average Loss {:.2f}%".format(self.total_packets, dropped_percentage),
              end='\r', flush=True)

    def effect(self, packet):
        """This function will issue packet loss,
           a percentage is defined and anything
           lower is dropped and anything higher is accepted"""

        # random value from 0 to 100
        random_value = random.uniform(0, 100)

        self.print_stats()

        self.total_packets += 1

        # If the generated value is smaller than the percentage discard
        if self.packet_loss_percentage > random_value:
            self.dropped_packets += 1
            packet.drop()

        # Accept the packet
        else:
            if self.accept:
                packet.accept()

    def alter_percentage(self, new_value):
        print('Packet loss: {}% -- '.format(new_value), flush=True, end='')
        self.packet_loss_percentage = new_value
