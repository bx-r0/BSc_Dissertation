import random


class Connection:
    """Container Class for real world connection types"""

    def __init__(self, l, pl, name):

            if len(l) is not 2 or len(pl) is not 2:
                raise Exception('Invalid parameters passed for Connection object!')

            self.latency = l
            self.packetloss = pl
            self.name = name

    @staticmethod
    def rnd(p_list):
        """Returns a random value in the given range"""

        low = p_list[0]
        high = p_list[1]

        return random.randint(low, high)


# TODO: Add accurate values
# Hard coded real-world values
#   The values are specified as lists representing ranges
v_3G = Connection([10, 20], [2, 5], '3G')
v_4G = Connection([0, 5], [1, 10], '4G')

# List of connection types
# Dynamically grabs the list of variables from the local list
# 'v_' Is used to identify connection variables in the local list
connections = [item for item in locals() if item.startswith("v_")]
