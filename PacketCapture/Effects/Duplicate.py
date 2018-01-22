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
        # TODO: Add stats - what would be useful?
        self.print('Duplicate')

    def effect(self, packet):

        # TODO needs fixing
        # Get packet data
        pkt = IP(packet.get_payload())

        pkt[IP].dst = "192.168.1.1"

        del pkt[ICMP].chksum
        del pkt[IP].chksum

        send(pkt, verbose=1, count=self.duplication_factor)

    # Graphing
        # TODO: Add graphing to Duplicate

    # Alter effect
        # TODO: Add alter effect to Duplicate
