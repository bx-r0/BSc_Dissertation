#region Imports
import os
import sys
from multiprocessing.pool import ThreadPool
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Packet
from Terminal import Terminal
import csv
from functools import partial
from datetime import datetime
import signal
from contextlib import contextmanager
import wget
from Effects.PacketLoss import PacketLoss
import time
#endregion


class Base_Test():
    """This class is used as a base class for test, the child class needs to overwrite the custom_test_behavior() method
    to add what it needs to do per test. The looping and number of tests is handled by the start() method"""

    def __init__(self, file_name_id,
                 start_effect_value,
                 max_effect_value,
                 effect_step,
                 repeat_tests,
                 max_test_time,
                 data_headers,
                 print_time_estimate=True):

        self.pool = ThreadPool(1000)
        self.time_str = self.grab_time_str()

        self.file_name_id = file_name_id

        self.START_EFFECT_VALUE = start_effect_value
        self.MAX_EFFECT_VALUE = max_effect_value
        self.EFFECT_STEP = effect_step
        self.REPEAT_TESTS = repeat_tests
        self.MAX_TEST_TIME = max_test_time

        if print_time_estimate:
            self.calculate_script_run_time()

        self.add_data_headers(data_headers)

    def start(self):
        # Test with a new packet value
        for effect_value in range(self.START_EFFECT_VALUE, self.MAX_EFFECT_VALUE + 1, self.EFFECT_STEP):

            test_data = []

            # Repeats for that percentage values
            for x in range(0, self.REPEAT_TESTS):

                Terminal.clear_line()
                print('\n## Starting test {}'.format(x))

                # CUSTOM BEHAVIOUR
                self.custom_test_behavior(effect_value, test_data)
                self.stop_pool()

            if test_data is not None:
                test_data.insert(0, effect_value)
                self.save_csv(test_data)

        print('## Tests done!')
        Terminal.clear_line()

    def custom_test_behavior(self, effect_value, test_data):
        """[Blueprint] Where the data and values are obtained and returned to the calling start method that will
        save the values and perform a clean-up"""
        return test_data

    def add_data_headers(self, data_headers):
        """Method used to add headers to the data in the .csv"""
        list = data_headers[:1] + (data_headers[1:] * self.REPEAT_TESTS)
        self.save_csv(list)

    def stop_pool(self):
        self.pool.terminate()

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

    @staticmethod
    def force_print(msg):
        """Overcomes the printing block to print important messages"""

        Base_Test.printing(True)
        print(msg)
        Base_Test.printing(False)

    @contextmanager
    def time_limit(self, seconds):
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
    def tcp_requests():
        """This performs a FTP Download to test TCP"""

        link = 'ftp://speedtest.tele2.net/'

        #filename = '1KB.zip'
        #filename = '100KB.zip'
        filename = '512KB.zip'
        #filename = '5MB.zip'

        wget.download(link + filename)

        # Removed any downloaded files
        os.system('rm -rf {}'.format(filename))
        os.system('rm -rf *.tmp')

    def calculate_script_run_time(self):
        # Calculates total time
        total_time = ((self.MAX_EFFECT_VALUE - self.START_EFFECT_VALUE) / float(self.EFFECT_STEP)) * self.REPEAT_TESTS * self.MAX_TEST_TIME
        seconds = total_time
        mins = round(total_time / 60, 2)
        hours = round(mins / 60, 2)

        print("## This script will take: {} seconds".format(seconds))
        print("## This script will take: {} mins".format(mins))
        print("## This script will take: {} hours".format(hours))

    # --------------------- TEST TYPES
    def run_test_TCP(self, obj, packet_type):
        """This will run packet loss and return values of TCP retransmissions"""

        self.pool = ThreadPool(1000)
        self.printing(False)

        self.run_packet_script(obj, packet_type)

        with self.time_limit(self.MAX_TEST_TIME):
            try:
                self.tcp_requests()
            except Exception:

                # If the request timed out
                os.system('rm -rf *.tmp')
                self.force_print('## Timeout occurred! - Accuracy may be compromised')

        Terminal.clear_line()
        self.printing(True)

    def run_test_basic(self, obj, packet_type):
        """Just runs the effect"""

        self.pool = ThreadPool(1000)
        self.run_packet_script(obj, packet_type)
