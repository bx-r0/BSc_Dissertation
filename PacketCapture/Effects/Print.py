from Effects.Effect import Effect


class Print(Effect):

    def __init__(self, accept_packets=True, show_output=True, graphing=False, graph_type_num=0):
        super().__init__(accept_packets=accept_packets,
                         show_output=show_output,
                         graphing=graphing,
                         graph_type_num=graph_type_num)

    def custom_effect(self, packet):
        print('[!]', str(packet), flush=True)
        self.accept(packet)
