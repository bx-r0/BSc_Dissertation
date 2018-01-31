from Effects.Effect import Effect
from scapy.all import *


class Duplicate(Effect):
    """Used to duplicate packets as many times as the parameter specifies"""

    def __init__(self, duplication_factor, accept_packets=True, show_output=True, graphing=False, graph_type_num=0):
        super().__init__(accept_packets=accept_packets,
                         show_output=show_output,
                         graphing=graphing,
                         graph_type_num=graph_type_num)

        self.duplication_factor = duplication_factor

    def print_stats(self):
        self.print('[*] Duplicated: {}'.format(self.total_packets), end='\r')

    def custom_effect(self, packet):

        dst = "192.168.1.16"
        src = "192.168.1.14"
        try:
            pkt = IP(packet.get_payload())
            send(pkt, verbose=0, count=self.duplication_factor)

        except Exception as e:
            pass

        packet.accept()

    # Graphing
    # TODO: Add graphing to Duplicate

    # Alter effect
    # TODO: Add alter effect to Duplicate
