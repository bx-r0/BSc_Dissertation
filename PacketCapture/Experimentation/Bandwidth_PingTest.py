from BaseClasses.Base_PingTest import PingTest
from Effects.Bandwidth.LimitBandwidth import LimitBandwidth


# TODO: getting replicated verdict errors when running the test??
class Bandwidth_PingTest(PingTest):
    """Increases the bandwidth and tests the latency value, this needs to be performed with a high
    number of packets"""

    def __init__(self):
        super().__init__('PingTest',
                         max_effect_value=10000,
                         start_effect_value=1000,
                         effect_step=100,
                         repeat_tests=1,
                         data_headers=['Bandwidth limit (B/s)', 'Average Latency (ms)'],
                         max_test_time=10)

        self.NUMBER_OF_PINGS = 15

    def custom_test_behavior(self, effect_value, data):
        bandwidth_obj = LimitBandwidth(effect_value)

        self.printing(False)
        self.run_test_basic(bandwidth_obj, 'ICMP')
        ping_values = self.grab_ping_value()
        self.printing(True)
        print(ping_values)

        average_ping = sum(ping_values) / len(ping_values)
        data.append(average_ping)

        print('Average ping value: {}'.format(average_ping))

        return data


test = Bandwidth_PingTest()
test.start()