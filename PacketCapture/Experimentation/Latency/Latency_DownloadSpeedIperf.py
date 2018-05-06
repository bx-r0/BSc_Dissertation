import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.Latency import Latency
import wget
import time


class DownloadSpeed(Base_Test):

    def __init__(self):
        super().__init__('DownloadSpeedIperf',
                         max_effect_value=1000,
                         start_effect_value=10,
                         effect_step=10,
                         repeat_tests=1,
                         data_headers=['Latency value (ms)', 'Bandwidth MBytes/sec', 'Total Transferred MBytes'],
                         max_test_time=60,
                         print_time_estimate=False)

    def custom_test_behavior(self, effect_value, data):

        latency_obj = Latency(effect_value)
        IperfResults = self.run_iperf_local(latency_obj, 'TCP')

        data.append(IperfResults.bandwidth)
        data.append(IperfResults.total_transferred)

        return data


test = DownloadSpeed()
test.start()
