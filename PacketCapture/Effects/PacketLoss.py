import random


class PacketLoss:

    def __init__(self, percentage, accept):
        self.packet_loss_percentage = int(percentage)
        self.accept = accept
        print('[*] Packet loss set to: {}%'.format(percentage), flush=True)

    def effect(self, packet):
        """This function will issue packet loss,
           a percentage is defined and anything
           lower is dropped and anything higher is accepted"""

        # random value from 1 to 100
        random_value = random.uniform(1, 100)

        # If the generated value is smaller than the percentage discard
        if self.packet_loss_percentage > random_value:
            print("[!] Packet dropped!", flush=True)

            packet.drop()

        # Accept the packet
        else:
            if self.accept:
                packet.accept()

    def alter_percentage(self, new_value):
        print('Packet loss: {}% -- '.format(new_value), flush=True, end='')
        self.packet_loss_percentage = new_value
