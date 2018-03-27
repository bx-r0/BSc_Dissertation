#region Imports
import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLoss import PacketLoss
#endregion Imports

"""
# ============================= # TEST SCRIPT # ============================= # 
Description:
    Test that increases packet loss while keeping track of retransmissions

Testing Method:

Values obtained:

# =========================================================================== # 
"""


class PacketLossRetranTest(Base_Test):
    """Test that increases the packet loss and obtains the values for retransmissions"""

    def __init__(self):
        super().__init__('PacketLossRetran',
                         max_effect_value=25,
                         start_effect_value=1,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)', 'No Retransmissions', 'Total Packets', 'Ratio'],
                         max_test_time=120)

    def custom_test_behavior(self, packet_loss_value, data):
        """
        This is run from the start() method in the Base_Test.py
        :param packet_loss_value: - The value of the effect
        :param data: - The list that will be saved to a .csv file
        :return: Returns the altered data to be used in the .csv
        """

        packet_loss_obj = PacketLoss(packet_loss_value)
        IperfResult = self.run_iperf_local(packet_loss_obj, 'TCP')
        total_packets = packet_loss_obj.total_packets

        ratio = 0
        if total_packets != 0:
            ratio = IperfResult.retransmissions / total_packets

        data.append(IperfResult.retransmissions)
        data.append(total_packets)
        data.append(ratio)

        # Displays data
        print('## Output: R:{} T:{} Ratio:{}'.format(IperfResult.retransmissions, total_packets, ratio * 100))

        return data


test = PacketLossRetranTest()
test.start()
