#region Imports
import os
import sys
from multiprocessing.pool import ThreadPool
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Effects.PacketLoss import PacketLoss
from Effects.Print import Print
import Packet
from Terminal import Terminal
import csv
from functools import partial
import wget
from datetime import datetime
import threading
import signal
from contextlib import contextmanager
#endregion


class Base_Test():

    def __init__(self, file_name_id):

        self.pool = ThreadPool(100)
        self.time_str = self.grab_time_str()

        self.file_name_id = file_name_id

    @staticmethod
    def printing(printing_on):
        """Used to stop printing when it isn't needed"""

        Terminal.clear_line()

        if printing_on:
            sys.stdout = sys.__stdout__
        else:
            sys.stdout = open(os.devnull, 'w')

    @staticmethod
    def grab_time_str():
        """Used to obtain a unique ID that corresponds to the time of day
        This is used when saving files"""

        # Grabs the random name of the file
        time_str = str(datetime.now())
        parts = time_str.split(' ')
        time_str = parts[0] + '_' + parts[1]
        time_str = time_str.split('.')[0]
        return time_str

    @staticmethod
    @contextmanager
    def time_limit(seconds):
        """This allows to run code for a certain amount of time
        Taken form the great answer at: http://bit.ly/2nQv9I7 by Josh Lee"""

        def signal_handler(signum, frame):
            raise TimeoutError("Timed out!")

        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)

    def save_csv(self, data):
        """Used when saving data to a .csv file"""

        print('## Saving.....', end='')

        # Saves the data
        with open('CSV/{}_{}.csv'.format(self.file_name_id, self.time_str), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data)

        print('[X]')

    def run_packet_script(self, obj, target_type='ALL'):
        """Used to run the Packet.py script with any object that is passed to this method"""

        func = partial(Packet.run_packet_manipulation_external, obj, target_type)
        self.pool.apply_async(func, [])

    def stop_pool(self):
        self.pool.terminate()