from Base_Test import Base_Test
from Effects.Latency import Latency
from Effects.Print import Print


class LatencyTimeOutTest(Base_Test):

    def __init__(self):
        super().__init__('LatencyTimeOutTest',
                         max_effect_value=10000,
                         start_effect_value=10,
                         effect_step=100,
                         repeat_tests=1,
                         max_test_time=60)

    def custom_test_behavior(self, latency_value, data):

        #latency_obj = Print()
        latency_obj = Latency(latency_value)
        self.run_test_TCP(latency_obj, 'TCP')

        # Grabs retransmissions
        retransmissions = latency_obj.retransmission
        total_packets = latency_obj.total_packets
        ratio = (retransmissions / total_packets) * 100

        # Saves data
        data.append(retransmissions)
        data.append(total_packets)
        data.append(ratio)

        # Displays data
        print('## Output: R:{} T:{} Ratio: {}'.format(retransmissions, total_packets, ratio))

        return data


test = LatencyTimeOutTest()
test.start()
