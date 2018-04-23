import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.Latency import Latency
import wget
import time


class PageLoadTest(Base_Test):

    def __init__(self):
        super().__init__('PageLoadTest',
                         max_effect_value=10000,
                         start_effect_value=10,
                         effect_step=100,
                         repeat_tests=1,
                         data_headers=['Latency value (ms)', 'Page Load Time(s)'],
                         max_test_time=60)

    def custom_test_behavior(self, effect_value, data):

        web_address = "https://en.wikipedia.org/wiki/University_of_Hull"

        latency_obj = Latency(effect_value)
        self.run_test_basic(latency_obj, 'TCP')

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
