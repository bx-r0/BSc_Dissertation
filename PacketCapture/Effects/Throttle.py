import threading
import time

# TODO: ISSUES
# - For some reason the value printed as 'sent' is always twice the number that actually have been sent??
# - There needs to be a wait before the packet is added to the pool?? Maybe they're being added too quickly
class Throttle:

    def __init__(self, period):
        self.throttle_pool = []
        self.throttle_job = None

        self.throttle_period = period / 1000
        print('[*] Packet throttle delay set to {}s'.format(self.throttle_period), flush=True)

    def effect(self, packet):
        time.sleep(0.00001)
        self.throttle_pool.append(packet)

    def throttle_purge(self):
        """Event that purges the packet pool when the time has elapsed"""

        # Sends all packets!
        for x in self.throttle_pool:
            x.accept()

        pool_len = len(self.throttle_pool)

        if pool_len is not 0:
            print("[!] Packets sent. Number: {}".format(pool_len))

        self.throttle_pool = []
        self.start_purge_monitor()

    def start_purge_monitor(self):
        # Starts another thread
        self.throttle_job = threading.Timer(self.throttle_period, self.throttle_purge).start()

    def stop(self):
        self.throttle_job.cancel()
        print('[!] Throttle purge job stopped!', flush=True)
