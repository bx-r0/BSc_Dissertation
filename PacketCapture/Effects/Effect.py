from Plotting import Graph

class Effect:
    """Class that generally defines what an effect should contain """

    def __init__(self, accept_packets=True, show_output=True, graphing=False):
        self.accept_packet = accept_packets
        self.show_output = show_output
        self.graphing = graphing

        if self.graphing:
            self.graph = Graph()

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

    def show_graph(self):
        """Called to display the graph"""

        if self.graphing:
            self.graph.plot()

    def stop(self):
        """Called to stop the object"""
        pass
