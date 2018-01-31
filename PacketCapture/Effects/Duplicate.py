from Effects.Effect import Effect
from scapy.all import *


class Duplicate(Effect):

    def __init__(self, duplication_factor, accept_packets=True, show_output=True, graphing=False, graph_type_num=0):
        super().__init__(accept_packets=accept_packets,
                         show_output=show_output,
                         graphing=graphing,
                         graph_type_num=graph_type_num)

        self.duplication_factor = duplication_factor

    def print_stats(self):
        self.print('[*] Duplicated: {}'.format(self.total_packets), end='\r')

    def custom_effect(self, packet):

        pkt = IP(packet.get_payload())

        # This displays all the valid information, nothing that doesn't look right
        pkt.show()

        # TODO: Need to check that this is actually sending using another machine
        # Maybe the new packets being sent are being caught in the NFQUEUE?
        sendp(pkt, verbose=0)
        packet.drop()

    # Graphing
        # TODO: Add graphing to Duplicate

    # Alter effect
        # TODO: Add alter effect to Duplicate
