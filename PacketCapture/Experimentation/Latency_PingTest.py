import os
from BaseClasses.Base_PingTest import PingTest
from Effects.Latency import Latency
import subprocess


class LatencyPingTest(PingTest):
    """Test that looks for the accuracy in the simulation of latency"""

    def __init__(self):
        super().__init__('PingTest',
                         max_effect_value=10000,
                         start_effect_value=10,
                         effect_step=100,
                         repeat_tests=1,
                         max_test_time=60)

        self.NUMBER_OF_PINGS = 3

    def custom_test_behavior(self, effect_value, data):

        latency_obj = Latency(effect_value)

        self.printing(False)
        self.run_test_basic(latency_obj, 'ICMP')
        ping_values = self.grab_ping_value()
        self.printing(True)

        # Output
        average_latency = sum(ping_values) / len(ping_values)
        target_value = effect_value
        error = (average_latency / target_value) * 100
        error -= 100
        difference = average_latency - target_value

        data.append(average_latency)
        data.append(error)
        data.append(difference)

        print('Average: {:.2f} - Target: {:.2f} - Diff: {:.2f}ms - Error: {:.2f}%'.
              format(average_latency, target_value, difference, error))


test = LatencyPingTest()
test.start()