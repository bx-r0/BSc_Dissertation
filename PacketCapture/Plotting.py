import os
try:
    from matplotlib import pyplot as plt
except ImportError:
    print('\nError: cannot import matplotlib, please install here')
    print('https://matplotlib.org/users/installing.html\n')
    exit(0)

# TODO: Put download link on README for matplotlib


class Graph:
    """This class is used to make a new graph, it
    contains two lists for x and y values that can
    be viewed by using 'plot()'"""

    def __init__(self):
        self.fig = plt.figure()
        self.x = []
        self.y = []
        self.n_index = 0

        self.picture_filename = 'graph.png'

    # TODO: Is it possible to dynmaically find out who the user is?
    def show(self):
        self.fig.savefig(self.picture_filename)
        os.system('sudo -u user_1 feh graph.png')

    def add_points(self, x, y):
        """Used to add values to the potential plot points"""
        self.x.append(x)
        self.y.append(y)

    def add_point(self, y):
        self.x.append(self.n_index)
        self.n_index = self.n_index + 1

        self.y.append(y)

    def plot(self):
        """Adds all points to the graph, adds a line and displays the graph"""
        plt.plot(self.x, self.y, 'ro-')

        self.show()

    def points(self):
        """Adds all the points to the graph (with no line) and display the graph"""

        for i in range(0, len(self.x)):
            plt.plot(self.x[i], self.y[i], 'ro-')

        self.show()




