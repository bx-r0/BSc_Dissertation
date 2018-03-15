#region Imports
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLossTimeDrop import PacketLossTimeDrop
from Effects.PacketLoss import PacketLoss
from TcpCongestionControl import TcpCongestionControl
#endregion Imports


class PacketLossMultipleCongestionAlgo(Base_Test):
    """
    Test that runs tests for different congestion algorithms
    """

    def __init__(self):
        super().__init__('PacketLossMultipleCongestionAlgo',
                         max_effect_value=0,
                         start_effect_value=0,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=[],
                         max_test_time=120,
                         print_time_estimate=False)

        # Time gap between intervals
        # Note: Anything below: 0.5 pushes the output into a different format
        self.UPDATE_INTERVAL = 0.05
        self.PACKET_LOSS_INTERVAL = 1
        self.TEST_TIME = 2

    def custom_test_behavior(self, packet_loss_value, data):
        """
        This is run from the start() method in the Base_Test.py
        :param packet_loss_value: - The value of the effect
        :param data: - The list that will be saved to a .csv file
        :return: Returns the altered data to be used in the .csv
        """

        requested_info = ['Interval', 'Cwnd', 'Transfer', 'Bandwidth', 'Write', 'Err', 'Rtry', 'RTT']

        # NOTE: Command is needed to stop tcp from saving session stats
        os.system('sysctl -w net.ipv4.tcp_no_metrics_save=0')

        packet_loss_obj = PacketLossTimeDrop(self.PACKET_LOSS_INTERVAL, gather_stats=False, show_output=False)
        self.run_test(packet_loss_obj, requested_info, 'reno')

        packet_loss_obj = PacketLossTimeDrop(self.PACKET_LOSS_INTERVAL, gather_stats=False, show_output=False)
        self.run_test(packet_loss_obj, requested_info, 'cubic')

        return data

    def run_test(self, effect_obj, requested_info, congestion_algo):
        """
        Runs the test with required data and congestion algorithm used
        :param effect_obj: - Effect object used to run the test
        :param requested_info: - The data headings required
        :param congestion_algo: - Name of the congestion algorithm
        :return:
        """

        TcpCongestionControl.set_algorithm(congestion_algo)
        IperfResult = self.run_iperf_multi(effect_obj, 'TCP', update_interval=self.UPDATE_INTERVAL, test_time=self.TEST_TIME)
        self.save_csv([''])
        self.save_csv([congestion_algo])
        for x in requested_info:
            self.add_data(IperfResult, x)

        TcpCongestionControl.reset()

    def add_data(self, IperfResult, key):
        """
        Saves a list of data to .csv
        :param IperfResult: - The IPERF test object
        :param key: - The name of the data in the dictionary
        :return:
        """

        cwnd_list = [key]
        for i in IperfResult.results_dict[key]:
            cwnd_list.append(i)
        self.save_csv(cwnd_list)


test = PacketLossMultipleCongestionAlgo()
test.start()
