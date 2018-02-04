#region Imports
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Effects.PacketLoss as PacketLoss
import Packet
#endregion


def run_test():
    """This will run packet loss and return values of TCP retansmissions"""

    # TODO: Get TCP Requests to perform automatically?

    packetLoss = PacketLoss.PacketLoss(1)
    try:
        Packet.run_packet_manipulation_external(packetLoss)
    except:
        print(packetLoss.retransmission)

run_test()
