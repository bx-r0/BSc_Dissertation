#region Imports
import os
import sys
from multiprocessing.pool import ThreadPool
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Effects.PacketLoss import PacketLoss
from Effects.Print import Print
import Packet
from Terminal import Terminal
import urllib.request as ul
import csv
from functools import partial
#endregion


def printing(printing_on):
    """Used to stop printing when it isn't needed"""

    Terminal.clear_line()

    if printing_on:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')


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


def run_packet_script(obj, target_type):
    func = partial(Packet.run_packet_manipulation_external, obj, target_type)
    pool.apply_async(func, [])


def request_webpage():
    req = ul.Request('https://coinmarketcap.com/')
    response = ul.urlopen(req)


def run_test(packet_loss):
    """This will run packet loss and return values of TCP retansmissions"""
    global pool

    pool = ThreadPool(100)

    try:
        printing(False)
        packetLoss = PacketLoss(packet_loss)
        run_packet_script(packetLoss, 'TCP')

        pool.apply_async(request_webpage)

        time.sleep(TEST_TIME)
        printing(True)

        return packetLoss
    except Exception as e:
        print('Error:', e)


TESTS = []
TEST_PER_VALUE = 3
MAX_PERCENTAGE_VALUE = 100
PERCENTAGE_STEP = 1
TEST_TIME = 15  # Seconds

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

    # Repeats for that percentage values
    for x in range(0, TEST_PER_VALUE):

        test = []
        test = [packet_loss]

        print('## Starting test {}'.format(x))
        packetLoss_obj = run_test(packet_loss)

        retransmissions = packetLoss_obj.retransmission
        total_packets = packetLoss_obj.total_packets
        ratio = (retransmissions / total_packets) * 100

        print('## Output: R:{} T:{} Ratio: {}'.format(retransmissions, total_packets, ratio))

        test.append(retransmissions)
        test.append(total_packets)
        test.append(ratio)

        pool.terminate()

        # Save after every test
        save_csv(test)

    TESTS.append(test)

print('## Tests done!')
Terminal.clear_line()