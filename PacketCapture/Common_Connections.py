import random


class Connection:
    """Container Class for real world connection types"""

    def __init__(self, l, pl, b, name):

            # Loops through and checks parameter lengths
            incorrect = (x for x in [l, pl, b] if not self.check_parameters(x))
            for value in incorrect:
                raise Exception('Invalid parameters passed for Connection object: {}!'.format(value))

            self.latency = l
            self.packetloss = pl
            self.bandwidth = b
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
v_3G = Connection([10, 20], [100, 200], [2, 5], '3G')
v_4G = Connection([0, 5], [1000, 2000], [1, 10], '4G')

# List of connection types
connections = [v_3G, v_4G]
