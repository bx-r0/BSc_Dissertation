import time
from Effects.Effect import Effect


class PacketLossTimeDrop(Effect):

    def __init__(self, percentage,
                 accept_packets=True,
                 show_output=True,
                 graphing=False,
                 gather_stats=True,
                 graph_type_num=False):

        super().__init__(accept_packets=accept_packets,
                         show_output=show_output,
                         graphing=graphing,
                         gather_stats=gather_stats,
                         graph_type_num=graph_type_num)

        self.packet_loss_percentage = int(percentage)
        self.print('[*] Packet loss set to: {}%'.format(percentage), force=True)

        # Stats
        self.total_packets = 0
        self.time_since_last_drop = -1

        self.DROP_INTERVAL_SECONDS = 5

    def custom_effect(self, packet):
        """This function will issue packet loss,
           a percentage is defined and anything
           lower is dropped and anything higher is accepted"""

        # Initial set
        if self.time_since_last_drop is -1:
            self.time_since_last_drop = time.time()
            self.accept(packet)
        else:
            elapsed = time.time() - self.time_since_last_drop

            if elapsed > self.DROP_INTERVAL_SECONDS:
                packet.drop()
                self.time_since_last_drop = time.time()
            else:
                self.accept(packet)