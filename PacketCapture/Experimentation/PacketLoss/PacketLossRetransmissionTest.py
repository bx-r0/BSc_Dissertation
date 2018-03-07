#region Imports
import os
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLoss import PacketLoss
#endregion Imports


class PacketLossRetranTest(Base_Test):
    """Test that increases the packet loss and obtains the values for retransmissions"""

    def __init__(self):
        super().__init__('PacketLossRetran',
                         max_effect_value=100,
                         start_effect_value=1,
                         effect_step=1,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)', 'No Retransmissions', 'Total Packets', 'Ratio'],
                         max_test_time=120)

    def custom_test_behavior(self, packetLoss_value, data):
        """This is run from the start() method in the Base_Test.py"""

        start_retransmission = self.get_current_retransmission_value()

        packet_loss_obj = PacketLoss(packetLoss_value)
        self.run_iperf_local(packet_loss_obj, 'TCP')

        end_retransmission = self.get_current_retransmission_value()
        total_retransmission = end_retransmission - start_retransmission

        total_packets = packet_loss_obj.total_packets

        ratio = total_retransmission / total_packets

        data.append(total_retransmission)
        data.append(total_packets)
        data.append(ratio)

        # Displays data
        print('## Output: R:{} T:{} Ratio:{}'.format(total_retransmission, total_packets, ratio))

        return data

    @staticmethod
    def get_current_retransmission_value():
        """
        Grabs the current retransmission value by querying netstat
        :return: Current retransmission value
        """

        import re

        # Runs the command
        cmd = "netstat -s | grep -i ret"
        retr = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # Finds all the values in the string
        value = map(int, re.findall(r'\d+', retr))

        # Adds up all the values
        total = 0
        for x in value:
            total += x

        return total



test = PacketLossRetranTest()
test.start()
