from Base_Test import Base_Test


class PacketLossWindowSize(Base_Test):

    def __init__(self):
        super().__init__('PacketLossWindowSize',
                         max_effect_value=100,
                         start_effect_value=1,
                         effect_step=9,
                         repeat_tests=1,
                         max_test_time=30)

    def custom_test_behavior(self, packetLoss_value, data):
        """Custom behavior for the test that is called from the start() method in the super"""

        packetLoss_obj = self.run_test_TCP(packetLoss_value)

        # Grabs the window sizes
        tcp_session = packetLoss_obj.tcp_sessions[0]

        # Gets the average window size
        total = 0
        for x in tcp_session.previous_packets:
            total += x.window_size
        avg_window_size = total / len(tcp_session.previous_packets)

        print('Output: Avg Window Size: {}'.format(avg_window_size))
        data.append(avg_window_size)

        return data

test = PacketLossWindowSize()
test.start()
