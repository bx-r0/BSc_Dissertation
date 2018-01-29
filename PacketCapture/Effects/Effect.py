import time
import Parameters
from Plotting import Graph
from scapy.all import *


class Effect:
    """Class that generally defines what an effect should contain """

    def __init__(self,
                 accept_packets=True,
                 show_output=True,
                 graphing=False,
                 graph_type_num=0):

        self.accept_packet = accept_packets
        self.show_output = show_output
        self.graphing = graphing
        self.graph_type_num = graph_type_num

        if self.graphing:

            self.graph = Graph()
            self.default_graphing_setup()

            if show_output:
                description = self.check_for_graph_type()
                print("""[*] Graph number is \'{}\' and the description is: \n[*]\t\"{}\"""".
                      format(self.graph_type_num, description))

        # --- Universal stats --- #
        # Every effect has a starting time
        self.start_time = time.time()
        self.total_packets = 0  # Number of total packets processed

        self.tcp_flags = []
        self.tcp_sessions = []
        self.retransmissions = 0

    def effect(self, packet):
        """The first method run for all effects - Here custom code will be added
        to collate information"""

        # TCP tracking
        self.track_TCP_stats(packet)

        # Shared functionality between all effects
        self.print_stats()
        self.total_packets += 1
        self.default_graphing(packet)
        self.custom_effect(packet)

    def custom_effect(self, packet):
        """Each effect will need it's own custom effect"""
        raise Exception('NotImplemented: Please add \'custom_effect()\' to your class')

    def print_stats(self):
        """[Blueprint] - Should print the custom stats for each method.
        Note Print_stats should call 'self.print()' to show any output """
        pass

    def check_for_graph_type(self):
        """This method checks for the graph number provided is valid"""
        class_name = self.__class__.__name__

        for x in Parameters.graph_descriptions:
            graph = x

            if graph.effect_name is class_name or graph.effect_name is None:
                if graph.number is self.graph_type_num:
                    return graph.description

        # If a graph cannot be found
        print('\n[ERROR] Invalid graph number provided\n')
        exit(0)

    def get_elapsed_time(self):
        """Used to find out how long ago the effect started"""
        return time.time() - self.start_time

    def print(self, message, end='\n', force=False):
        """General print method"""
        if self.show_output or force:
            print(message, end=end, flush=True)

    @staticmethod
    def print_clear():
        """Method that is used to clear the output line, this is
        so no fragments are left after a stat print refresh"""
        print(' ' * 70, end='\r', flush=True)

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

    # Variance
    def increase_effect(self):
        """[Blueprint] - Used to make the degradation higher """
        pass

    def decrease_effect(self):
        """[Blueprint] - Used to make the degradation lower"""
        pass

    def check_packet_type(self, packet, target_packet):
        """Checks if the packet is of a certain type"""

        # Grabs the first section of the Packet
        packet_string = str(packet)
        split = packet_string.split(' ')

        # Checks for the target packet type
        if target_packet == split[0]:
            return True
        else:
            return False

    # Stats
    def track_TCP_stats(self, packet):
        """Method that tracks characteristics of the TCP packets """

        try:
            self.check_for_retransmissions(packet)
        except Exception as e:
            pass

    def check_for_retransmissions(self, packet):
        """This method checks for any TCP packets that
        have been retransmitted"""

        pkt = IP(packet.get_payload())

        # IPs
        dst = pkt.dst
        src = pkt.src

        # Ports
        dst_port = pkt.dport

        # Sequence number
        seq_num = pkt.seq

        # ACK Number
        ack_num = pkt.ack

        # Creates the session object
        session = TCP_Session(dst, dst_port, src, seq_num, ack_num, len(pkt))
        flags = session.get_flags(packet)

        # 3rd position is the RST flag
        # It will ignore the session if it is a RST packet
        if flags[2] is None:
            any_connection = True

            # Loops through the collected list of distinct sessions
            for x in self.tcp_sessions:

                # Checks if the SEQ and ACK values are correct
                if x.Check_For_Retransmit(session):

                    # Stops the connection from being saved
                    any_connection = False

                    self.retransmissions += 1

                    print(session)
                    break

            # Adds connections to the list
            if any_connection:
                self.tcp_sessions.append(session)


class TCP_Session:

    def __init__(self, dst_ip, dst_port, src_ip, seq_num, ack_num, size):
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.src_ip = src_ip

        self.seq_num = int(seq_num)
        self.ack_num = ack_num

        self.size = size

    def __str__(self):
        return "Dest: {} - Src: {} - DPort: {} - Seq: {} - Ack: {} - Size: {}".\
            format(self.dst_ip, self.src_ip, self.dst_port, self.seq_num, self.ack_num, self.size)

    def Check_For_Retransmit(self, connection):
        """Method that checks if the values are from the same connection"""

        dst_ip = connection.dst_ip
        dst_port = connection.dst_port
        src_ip = connection.src_ip

        if (self.dst_ip == dst_ip) and \
                (self.dst_port == dst_port) and \
                (self.src_ip == src_ip):
            return self.retransmit(connection.seq_num, connection.ack_num, connection.size)
        else:
            return False

    def retransmit(self, actual_seq_num, actual_ack_num, actual_size):
        """Method that checks for any problems in a sequence
        False - Not a Retransmit
        True - Is a Retransmit"""

        # If the packet is correct
        if (self.seq_num < actual_seq_num) and (self.ack_num <= actual_ack_num):

            # Updates sequence number
            self.seq_num = actual_seq_num

            # Updates ack number
            self.ack_num = actual_ack_num
            return False

        # If the packet is identical
        elif (self.seq_num == actual_seq_num) and \
                (self.ack_num == actual_ack_num) and \
                (self.size == actual_size):
            return True

        return False

    @staticmethod
    def get_flags(packet):
        FIN = 0x01
        SYN = 0x02
        RST = 0x04
        PSH = 0x08
        ACK = 0x10
        URG = 0x20
        ECE = 0x40
        CWR = 0x80

        pkt = IP() / TCP(packet.get_payload())
        flags = pkt['TCP'].flags

        # Saves the flags
        active_flags = [None] * 8
        if flags & FIN:
            active_flags[0] = 'FIN'
        if flags & SYN:
            active_flags[1] = 'SYN'
        if flags & RST:
            active_flags[2] = 'RST'
        if flags & PSH:
            active_flags[3] = 'PSH'
        if flags & ACK:
            active_flags[4] = 'ACK'
        if flags & URG:
            active_flags[5] = 'URG'
        if flags & ECE:
            active_flags[6] = 'ECE'
        if flags & CWR:
            active_flags[7] = 'CWR'

        return active_flags
