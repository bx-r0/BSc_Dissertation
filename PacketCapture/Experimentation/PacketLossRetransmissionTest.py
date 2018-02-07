from Base_Test import Base_Test


class PacketLossRetranTest(Base_Test):

    def __init__(self):
        super().__init__('PacketLossRetran',
                         max_effect_value=100,
                         start_effect_value=70,
                         effect_step=10,
                         repeat_tests=1,
                         max_test_time=60)

    def custom_test_behavior(self, packetLoss_value, data):
        """This is run from the start() method in the Base_Test.py"""

        packetLoss_obj = self.run_test_TCP(packetLoss_value)

        # Grabs data
        retransmissions = packetLoss_obj.retransmission
        total_packets = packetLoss_obj.total_packets
        ratio = (retransmissions / total_packets) * 100

        # Saves data
        data.append(retransmissions)
        data.append(total_packets)
        data.append(ratio)

        # Displays data
        print('## Output: R:{} T:{} Ratio: {}'.format(retransmissions, total_packets, ratio))

        return data


test = PacketLossRetranTest()
test.start()
