import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.Latency import PacketLoss
import wget
import time

class PageLoadTest(Base_Test):

    def __init__(self):
        super().__init__('PageLoadTest',
                         max_effect_value=100,
                         start_effect_value=1,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet Loss (ms)', 'Page Load Time(s)'],
                         max_test_time=60)

    def custom_test_behavior(self, effect_value, data):

        web_address = "https://en.wikipedia.org/wiki/University_of_Hull"

        packet_loss_obj = PacketLoss(effect_value)
        self.run_test_basic(packet_loss_obj, 'TCP')

        start_time = time.time()

        wget.download(web_address, bar=None)

        end_time = time.time()
        elapsed_time = end_time - start_time

        data.append(elapsed_time)

        # Removes Wget file
        os.system('rm -r University_of_Hull')

        return data


test = PageLoadTest()
test.start()
