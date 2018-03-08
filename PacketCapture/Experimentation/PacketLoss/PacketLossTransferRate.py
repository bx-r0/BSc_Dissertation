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


class PacketLossTransferRateTest(Base_Test):
    """Test that increases the packet loss and obtains the values for retransmissions"""

    def __init__(self):
        super().__init__('PacketLossTransferRate',
                         max_effect_value=25,
                         start_effect_value=1,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)', 'Algorithm', 'Bandwidth (Mbits/sec)', 'Total Transferred (MBytes)'],
                         max_test_time=120,
                         print_time_estimate=False)

    def custom_test_behavior(self, packet_loss_value, data):
        """
        This is run from the start() method in the Base_Test.py
        :param packet_loss_value: - The value of the effect
        :param data: - The list that will be saved to a .csv file
        :return: Returns the altered data to be used in the .csv
        """

        packet_loss_obj = PacketLoss(packet_loss_value)
        IperfResult = self.run_iperf_local(packet_loss_obj, 'TCP')

        bandwidth = IperfResult.bandwidth
        transfer = IperfResult.total_transferred

        data.append(TcpCongestionControl.get_algorithm())
        data.append(bandwidth)
        data.append(transfer)

        print('## Output: Bandwidth: {} Mbits/sec - Transferred: {} MB'.
              format(bandwidth, transfer))

        return data


test = PacketLossTransferRateTest()
test.start()
