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
            self.default_graphing_setup()

            if show_output:
                print('[*] Graph set to mode \'{}\''.format(graph_type_num))

        # --- Universal stats --- #
        # Every effect has a starting time
        self.start_time = time.time()
        self.total_packets = 0  # Number of total packets processed

    def get_elapsed_time(self):
        """Used to find out how long ago the effect started"""
        return time.time() - self.start_time

    def print(self, message, end='\n', force=False):
        """General print method"""
        if self.show_output or force:
            print(message, end=end, flush=True)

    def accept(self, packet):
        """Center point for accepting packets"""
        self.total_packets += 1

        if self.accept_packet:
            packet.accept()

    def default_graphing(self, packet):
        """The main functionality for all the effects, where graphing is available"""

        if self.graphing:
            # Graph that tracks types of packets in the session
            if self.graph_type_num is 0:
                sections = str(packet).split(' ')
                self.graph.increment_catagory(sections[0])

            # Graph that processes total number of packets over time
            elif self.graph_type_num is 10:
                self.graph.add_points(self.get_elapsed_time(), self.total_packets)

            # Each effects custom graphing
            else:
                self.graphing_effect(packet)

    def default_graphing_setup(self):
        """Used to init all axis and other variables required"""

        if self.graphing:
            # Graph that tracks types of packets in the session
            if self.graph_type_num is 0:
                self.graph.set_y_axis_label('Number of packets')

            # Graph that processes total number of packets over time
            elif self.graph_type_num is 10:
                self.graph.set_x_axis_label('Time (s)')
                self.graph.set_y_axis_label('Total Packets')
            else:
                self.graphing_setup()

    def show_default_graphs(self):
        # Graph that tracks types of packets in the session
        if self.graph_type_num is 0:
            self.graph.bar()

        # Graph that processes total number of packets over time
        elif self.graph_type_num is 10:
            self.graph.plot('g,-')

        else:
            self.show_custom_graph()

    def show_graph(self):
        """Called to display any type of graph"""
        self.show_default_graphs()

    def save_graph(self):
        """Will just save the graph to file"""
        self.graph.save()

    def print_stats(self):
        """[Blueprint] - Should print the custom stats for each method.
        Note Print_stats should call 'self.print()' to show any output """
        raise Exception('NotImplemented: Please add \'print_stats()\' to your class')

    def effect(self):
        """[Blueprint] - Should be the main center for the effects code"""
        raise Exception('NotImplemented: Please add \'effect()\' to your class')

    def graphing_setup(self):
        """[Blueprint] - Custom code for each effects graph setup"""
        pass

    def graphing_effect(self, packet):
        """[Blueprint] - Function that contains custom graph effects"""
        pass

    def show_custom_graph(self):
        """[Blueprint] - Each effect will change the behavior of this method to add it's own affects"""
        pass

    def stop(self):
        """[Blueprint] - Called to stop the object"""
        pass
