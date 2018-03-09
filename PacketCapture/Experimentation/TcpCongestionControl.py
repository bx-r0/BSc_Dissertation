import os
import subprocess


class TcpCongestionControl:

    """
    Algorithms:
        'reno'  -
        'cubic' -
    """

    @staticmethod
    def print_available_algorithms():
        for x in TcpCongestionControl.get_available_algorithms():
            print(x)

    @staticmethod
    def get_available_algorithms():
        cmd = "cat /proc/sys/net/ipv4/tcp_available_congestion_control"
        result = subprocess.check_output(cmd.split(' '))
        result_list = result.decode('utf-8').strip().split(' ')
        return result_list

    @staticmethod
    def set_algorithm(name):
        avaliable = TcpCongestionControl.get_available_algorithms()

        if not avaliable.__contains__(name):
            print("Error: Invalid algorithm name: \'{}\'".format(name))
        else:
            os.system('echo {} > /proc/sys/net/ipv4/tcp_congestion_control'.format(name))
            print("Congestion algorithm changed to \'{}\'!".format(name))

    @staticmethod
    def get_algorithm():

        cmd = 'cat /proc/sys/net/ipv4/tcp_congestion_control'
        result = subprocess.check_output(cmd.split(' '))

        return result.decode('utf-8').strip()

    @staticmethod
    def reset():
        """
        Sets back to the cubic default
        """
        os.system('echo cubic > /proc/sys/net/ipv4/tcp_congestion_control')



