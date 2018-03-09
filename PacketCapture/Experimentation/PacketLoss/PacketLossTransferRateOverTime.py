#region Imports
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLoss import PacketLoss
from TcpCongestionControl import TcpCongestionControl
#endregion Imports


class PacketLossTransferRateTestOverTime(Base_Test):
    """Test that increases the packet loss and obtains the values for retransmissions"""

    def __init__(self):
        super().__init__('PacketLossTransferRate',
                         max_effect_value=10,
                         start_effect_value=0,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)', 'Algorithm', 'Bandwidth (Mbits/sec)', 'Total Transferred (MBytes)'],
                         max_test_time=120,
                         print_time_estimate=False)

        # Time gap between intervals
        self.UPDATE_INTERVAL = 1
        self.TEST_TIME = 10

        self.CONGESTION_ALGO = 'reno'

    def custom_test_behavior(self, packet_loss_value, data):
        """
        This is run from the start() method in the Base_Test.py
        :param packet_loss_value: - The value of the effect
        :param data: - The list that will be saved to a .csv file
        :return: Returns the altered data to be used in the .csv
        """

        TcpCongestionControl.set_algorithm(self.CONGESTION_ALGO)

        packet_loss_obj = PacketLoss(packet_loss_value)

        IperfResult = self.run_iperf_multi(packet_loss_obj,
                                           'TCP',
                                           update_interval=self.UPDATE_INTERVAL)

        # TODO: Update column headers
        # TODO: Save Results

        TcpCongestionControl.reset()

        return data


test = PacketLossTransferRateTestOverTime()
test.start()
