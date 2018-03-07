    #region Imports
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLoss import PacketLoss
#endregion Imports


class PacketLossFTPDownload(Base_Test):

    def __init__(self):
        super().__init__('PacketLossFTPDownload',
                         max_effect_value=100,
                         start_effect_value=1,
                         effect_step=10,
                         repeat_tests=1,
                         max_test_time=250,
                         data_headers=['Packet Loss (%)', 'File download time (s)'],
                         print_time_estimate=False)

    def custom_test_behavior(self, effect_value, data):
        latency_obj = PacketLoss(effect_value)

        start = time.time()
        self.run_test_TCP(latency_obj, 'TCP')
        end = time.time()

        elapsed = end - start

        data.append(elapsed)
        print('Elapsed time: {:.2f} seconds'.format(elapsed))

        return data


test = PacketLossFTPDownload()
test.start()
