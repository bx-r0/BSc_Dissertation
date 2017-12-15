import threading
import random


class Order:

    def __init__(self):
        self.send_interval = 1

        self.packet_list = []
        self.active = True
        self.start_packet_send()

        self.total = 0

    def stats(self):
        print('[*] Total packets received {}'.format(self.total), end='\r', flush=True)

    def effect(self, packet):
        # Saves the packet
        self.packet_list.append(packet)
        self.total += 1
        self.stats()

    def send_packet(self):

        # Grabs a position in the list
        list_len = len(self.packet_list)

        # Sends and deletes the list
        while list_len > 0:
            index = random.randint(0, list_len - 1)
            self.packet_list[index].accept()
            del self.packet_list[index]

            list_len = len(self.packet_list)

        self.start_packet_send()

    def start_packet_send(self):
        self.job = threading.Timer(self.send_interval, self.send_packet).start()

    def stop(self):
       self.job.stop()
