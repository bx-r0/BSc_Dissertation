#region Imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from BaseClasses.Base_PingTest import PingTest
from Effects.Latency import Latency
#endregion Imports

"""
# ============================= # TEST SCRIPT # ============================= # 
Description:
    Test that is looking for accuracy of simulated latency

Testing Method:
    Localhost ping test

Values obtained:
    - Latency Value (Target)
    - Average latency
    - Error (%)
    - Difference (ms)
    - Data

# =========================================================================== # 
"""


class LatencyPingTest(PingTest):
    """Test that looks for the accuracy in the simulation of latency"""

    def __init__(self):
        super().__init__('PingTest',
                         max_effect_value=1000,
                         start_effect_value=1,
                         effect_step=10,
                         repeat_tests=1,
                         data_headers=['Latency value (ms)',
                                       'Average Latency',
                                       'Error',
                                       'Difference',
                                       'Raw Values'],
                         max_test_time=60,
                         print_time_estimate=False)

        self.NUMBER_OF_PINGS = 10

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

        # Adds raw values
        for x in ping_values:
            data.append(x)

        print('Average: {:.2f} - Target: {:.2f} - Diff: {:.2f}ms - Error: {:.2f}%'.
              format(average_latency, target_value, difference, error))


test = LatencyPingTest()
test.start()