#region Imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from BaseClasses.Base_Test import Base_Test
from Effects.PacketLoss import PacketLoss
#endregion Imports

"""
# ============================= # TEST SCRIPT # ============================= # 
Description:

Testing Method:

Values obtained:

# =========================================================================== # 
"""

class PacketLossWindowSize(Base_Test):
    """Test that compares Packet loss with the windows size of a packet"""

    def __init__(self):
        super().__init__('PacketLossWindowSize',
                         max_effect_value=100,
                         start_effect_value=0,
                         effect_step=10,
                         repeat_tests=1,
                         data_headers=['Packet loss (%)'],
                         max_test_time=120,
                         print_time_estimate=False)

    def custom_test_behavior(self, packetLoss_value, data):
        """Custom behavior for the test that is called from the start() method in the super"""

        print("[!] REMEMBER TO RUN iperf SERVER", )

        packetLoss_obj = PacketLoss(packetLoss_value)
        self.run_iperf_local(packetLoss_obj, 'TCP')

        # Grabs the window sizes
        tcp_session = packetLoss_obj.tcp_sessions[0]

        print("[!] Number of packets collected: ", len(packetLoss_obj.tcp_sessions[0].previous_packets))

        for x in tcp_session.previous_packets:

            if x.src_port == 5001:
                # Makes sure it's going one way
                data.append(x.window_size)

        return data


test = PacketLossWindowSize()
test.start()
