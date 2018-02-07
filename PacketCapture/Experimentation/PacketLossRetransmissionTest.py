#region Imports
import os
import sys
from multiprocessing.pool import ThreadPool
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Effects.PacketLoss import PacketLoss
from Terminal import Terminal
import wget
from datetime import datetime
from Base_Test import Base_Test
#endregion


class PacketLossRetranTest(Base_Test):

    def __init__(self):
        super().__init__('PL_RetranTest')

        self.TESTS = []
        self.TEST_PER_VALUE = 1
        self.MAX_PERCENTAGE_VALUE = 100
        self.PERCENTAGE_STEP = 5
        self.MAX_TEST_TIME = 15  # Seconds

    def start(self):
        # Test with a new packet value
        for packet_loss in range(1, self.MAX_PERCENTAGE_VALUE + 1, self.PERCENTAGE_STEP):
            print('\n## Packet loss now: {}%'.format(packet_loss))

            # Repeats for that percentage values
            for x in range(0, self.TEST_PER_VALUE):
                test = [packet_loss]

                print('## Starting test {}'.format(x))
                packetLoss_obj = self.run_test(packet_loss)

                retransmissions = packetLoss_obj.retransmission
                total_packets = packetLoss_obj.total_packets
                ratio = (retransmissions / total_packets) * 100

                print('## Output: R:{} T:{} Ratio: {}'.format(retransmissions, total_packets, ratio))

                test.append(retransmissions)
                test.append(total_packets)
                test.append(ratio)

                self.stop_pool()

                # Save after every test
                self.save_csv(test)

            self.TESTS.append(test)

        print('## Tests done!')
        Terminal.clear_line()

    def run_test(self, packet_loss):
        """This will run packet loss and return values of TCP retransmissions"""

        self.pool = ThreadPool(100)

        try:
            self.printing(False)

            packet_loss = PacketLoss(packet_loss)
            self.run_packet_script(packet_loss, 'TCP')

            with self.time_limit(self.MAX_TEST_TIME):

                try:
                    self.tcp_requests()
                except TimeoutError:
                    self.printing(True)
                    print('## Timeout occurred!')

            self.printing(True)

            return packet_loss
        except Exception as e:
            print('Error:', e)

    @staticmethod
    def calculate_script_run_time(self):
        # Calculates total time
        total_time = (self.MAX_PERCENTAGE_VALUE / float(self.PERCENTAGE_STEP)) * self.TEST_PER_VALUE * self.TEST_TIME
        seconds = total_time
        mins = round(total_time / 60, 2)
        hours = round(mins / 60, 2)

        print("## This script will take: {} seconds".format(seconds))
        print("## This script will take: {} mins".format(mins))
        print("## This script will take: {} hours".format(hours))


    def tcp_requests(self):
        """This performs a FTP Download to test TCP"""

        link = 'ftp://speedtest.tele2.net/'

        #filename = '1KB.zip'
        filename = '100KB.zip'
        #filename = '512KB.zip'
        #filename = '5MB.zip'

        wget.download(link + filename)

        # Removed any downloaded files
        os.system('rm -rf {}'.format(filename))
        os.system('rm -rf *.tmp')

test = PacketLossRetranTest()
test.start()
