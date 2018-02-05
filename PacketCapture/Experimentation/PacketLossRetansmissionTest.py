#region Imports
import os
import sys
from multiprocessing.pool import ThreadPool
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Effects.PacketLoss import PacketLoss
import Packet
from Terminal import Terminal
import urllib.request as ul
import csv
#endregion


def printing(printing_on):
    """Used to stop printing when it isn't needed"""

    Terminal.clear_line()

    if printing_on:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')


def terminate_script():
    Terminal.clear_line()
    print('[!] Script terminated')
    pool.close()


def save_csv(test):
    """
    Saves data to a .csv file
    The format is:
        <packet_loss_value> <retransmission_value>
    """

    print('## Saving.....', end='')

    # Saves the data
    with open('test.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(test)

    print('[X]')


def run_packet_script(obj):
    pool.apply_async(Packet.run_packet_manipulation_external, [obj])


def request_webpage():
    req = ul.Request('http://www.google.com')
    response = ul.urlopen(req)
    the_page = response.read()


def run_test(packet_loss):
    """This will run packet loss and return values of TCP retansmissions"""
    global pool

    pool = ThreadPool(100)

    try:
        printing(False)
        packetLoss = PacketLoss(packet_loss)
        run_packet_script(packetLoss)

        for x in range(1, 2):
            pool.apply_async(request_webpage, [])

        time.sleep(TEST_TIME)
        terminate_script()
        printing(True)

        return packetLoss.retransmission
    except Exception as e:
        print('Error:', e)


TESTS = []
TEST_PER_VALUE = 2
MAX_PERCENTAGE_VALUE = 1
PERCENTAGE_STEP = 1
TEST_TIME = 5  # Seconds

# Calculates total time
total_time = (MAX_PERCENTAGE_VALUE / float(PERCENTAGE_STEP)) * TEST_PER_VALUE * TEST_TIME
seconds = total_time
mins = round(total_time / 60, 2)
hours = round(mins / 60, 2)

print("## This script will take: {} seconds".format(seconds))
print("## This script will take: {} mins".format(mins))
print("## This script will take: {} hours".format(hours))

# Resets .csv file
with open('test.csv', 'w'):
    pass

# This code runs the tests
# '+1' Just so the loop goes up to that value

# Test with a new packet value
for packet_loss in range(1, MAX_PERCENTAGE_VALUE + 1, PERCENTAGE_STEP):
    print('\n## Packet loss now: {}%'.format(packet_loss))

    test = [packet_loss]

    # Repeats for that percentage values
    for x in range(0, TEST_PER_VALUE):

        print('## Starting test {}'.format(x))
        value = run_test(packet_loss)
        print('## Output: {}'.format(value))
        test.append(value)

        # Save after every test
        save_csv([packet_loss, value])

    TESTS.append(test)

print('## Tests done!')
Terminal.clear_line()