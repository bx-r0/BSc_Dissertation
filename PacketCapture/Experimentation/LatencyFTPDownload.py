import time
from BaseClasses.Base_Test import Base_Test
from Effects.Latency import Latency


class LatencyFTPDownload(Base_Test):
    """Checks the download time for 512KB file.
    CSV Format:
        <effect_value> <download_time>(S)"""

    def __init__(self):
        super().__init__('LatencyFTPDownload',
                         max_effect_value=3000,
                         start_effect_value=10,
                         effect_step=100,
                         repeat_tests=2,
                         max_test_time=250,
                         data_headers=['Latency value (ms)', 'File download time (s)'],
                         print_time_estimate=False)

    def custom_test_behavior(self, effect_value, data):
        latency_obj = Latency(effect_value)

        start = time.time()
        self.run_test_TCP(latency_obj, 'TCP')
        end = time.time()

        elapsed = end - start
        print('Elapsed time: {:.2f} seconds'.format(elapsed))

        data.append(elapsed)

        return data


test = LatencyFTPDownload()
test.start()
