import random


class Connection:
    """Container Class for real world connection types"""

    def __init__(self, latency, packet_loss, bandwidth, name):

            # Loops through and checks parameter lengths
            incorrect = (x for x in [latency, packet_loss, bandwidth] if not self.check_parameters(x))
            for value in incorrect:
                raise Exception('Invalid parameters passed for Connection object: {}!'.format(value))

            self.latency = latency
            self.packetloss = packet_loss
            self.bandwidth = bandwidth
            self.name = name

    @staticmethod
    def check_parameters(parameter):
        if len(parameter) is 2:
            return True
        else:
            return False

    def rnd_latency(self):
        return self.rnd(self.latency) / 1000

    def rnd_packet_loss(self):
        return int(self.rnd(self.packetloss))

    def rnd_bandwidth(self):
        return int(self.rnd(self.bandwidth))

    @staticmethod
    def rnd(p_list):
        """Returns a random value in the given range"""

        low = p_list[0]
        high = p_list[1]

        return random.randint(low, high)


# TODO: Add accurate values
# Hard coded real-world values
#   The values are specified as lists representing ranges
_3G = Connection(
    latency=[200, 250],
    bandwidth=[600, 1000],
    packet_loss=[1, 2],
    name='3G')

_4G = Connection(
    latency=[100, 150],
    bandwidth=[10000, 15000],
    packet_loss=[0.5, 1],
    name='4G')

_GPRS = Connection(
    latency=[400, 500],
    bandwidth=[40, 50],
    packet_loss=[1, 2],
    name='GPRS')

_WIFI = Connection(
    latency=[30, 40],
    bandwidth=[25000, 30000],
    packet_loss=[0, 1],
    name='WIFI')

_NoConnection = Connection(
    latency=[0, 0],
    bandwidth=[0, 0],
    packet_loss=[100, 100],
    name='NoConnection')


# List of connection types
connections = \
    [
        _3G,
        _4G,
        _GPRS,
        _WIFI,
        _NoConnection
    ]
