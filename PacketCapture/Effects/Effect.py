import time
from Plotting import Graph


class Effect:
    """Class that generally defines what an effect should contain """

    def __init__(self, accept_packets=True, show_output=True, graphing=False, graph_type_num=0):
        self.accept_packet = accept_packets
        self.show_output = show_output
        self.graphing = graphing
        self.graph_type_num = graph_type_num

        if self.graphing:
            self.graph = Graph()
            self.graphing_setup()

            if show_output:
                print('[*] Graph set to mode \'{}\''.format(graph_type_num))

        # Every effect has a starting time
        self.start_time = time.time()

    def get_elapsed_time(self):
        """Used to find out how long ago the effect started"""
        return time.time() - self.start_time

    def print(self, message, end='\n', force=False):
        """General print method"""
        if self.show_output or force:
            print(message, end=end, flush=True)

    def accept(self, packet):
        """Center point for accepting packets"""
        if self.accept_packet:
            packet.accept()

    def print_stats(self):
        """Blueprint method: Should print the custom stats for each method.
        Note Print_stats should call 'self.print()' to show any output """
        raise Exception('NotImplemented: Please add \'print_stats()\' to your class')

    def effect(self):
        """Should be the main center for the effects code"""
        raise Exception('NotImplemented: Please add \'effect()\' to your class')

    def default_graphing(self, packet):
        """The main functionality for all the effects, where graphing is available"""

        # Graph that tracks types of packets in the session
        if self.graphing:
            if self.graph_type_num is 0:
                sections = str(packet).split(' ')
                self.graph.increment_catagory(sections[0])
            else:
                self.graphing_effect(packet)

    def graphing_setup(self):
        """Used to init all axis and other variables required"""
        pass

    def graphing_effect(self, packet):
        """Function that contains custom graph effects"""
        pass

    def show_graph(self):
        """Called to display any type of graph"""
        pass

    def stop(self):
        """Called to stop the object"""
        pass
