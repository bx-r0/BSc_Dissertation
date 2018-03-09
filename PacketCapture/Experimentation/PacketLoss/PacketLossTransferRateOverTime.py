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


class PacketLossTransferRateTestOverTime(Base_Test):
    """Test that increases the packet loss and obtains the values for retransmissions"""

    def __init__(self):
        super().__init__('PacketLossTransferRateOverTime',
                         max_effect_value=5,
                         start_effect_value=0,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)'],
                         max_test_time=120,
                         print_time_estimate=False)

        # Time gap between intervals
        # Note: Anything below: 0.5 pushes the output into a different format
        self.UPDATE_INTERVAL = 0.3
        self.TEST_TIME = 10

        self.CONGESTION_ALGO = 'reno'

    # Dictionary Options
    # ------------------
    # Interval
    # Transfer
    # Bandwidth
    # Write
    # Err
    # Rtry
    # Cwnd
    # RTT

    def custom_test_behavior(self, packet_loss_value, data):
        """
        This is run from the start() method in the Base_Test.py
        :param packet_loss_value: - The value of the effect
        :param data: - The list that will be saved to a .csv file
        :return: Returns the altered data to be used in the .csv
        """

        TcpCongestionControl.set_algorithm(self.CONGESTION_ALGO)

        packet_loss_obj = PacketLossTimeDrop()

        IperfResult = self.run_iperf_multi(packet_loss_obj,
                                           'TCP',
                                           update_interval=self.UPDATE_INTERVAL)

        data.append('Interval')
        for x in IperfResult.results_dict['Interval']:
            data.append(x)

        data.append('Cwnd')
        for x in IperfResult.results_dict['Cwnd']:
            data.append(x)

        TcpCongestionControl.reset()

        return data


test = PacketLossTransferRateTestOverTime()
test.start()
