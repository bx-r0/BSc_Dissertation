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
#endregion

pool = ThreadPool(100)


def terminate_script():
    Terminal.clear_line()
    print('[!] Script terminated')
    pool.close()


def run_test():
    """This will run packet loss and return values of TCP retansmissions"""

    # TODO: Get TCP Requests to perform automatically?

    packetLoss = PacketLoss(1)

    try:
        pool.map_async(Packet.run_packet_manipulation_external, [packetLoss])

        time.sleep(10)

        terminate_script()
    
        print(packetLoss.retransmission)
    except Exception as e:
       print('Error:', e)


run_test()
