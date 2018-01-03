from Effects.Effect import Effect
import threading
import time


class Throttle(Effect):

    def __init__(self, period, accept_packet=True, show_output=True):
        super().__init__(accept_packet, show_output)

        # General vars
        self.throttle_pool = []
        self.throttle_job = None
        self.throttle_period = period / 1000

        self.print('[*] Packet throttle delay set to {}s'.format(self.throttle_period), force=True)

    def effect(self, packet):
        """General effect"""

        # HACK: Why is this wait needed?
        time.sleep(0.00001)
        self.throttle_pool.append(packet)

    def throttle_purge(self):
        """Event that purges the packet pool when the time has elapsed"""

        # Sends all packets!
        for x in self.throttle_pool:
            self.accept(x)

        pool_len = len(self.throttle_pool)

        if pool_len is not 0:
            self.print("[!] Packets sent. Number: {}".format(pool_len), end='\r')

        self.throttle_pool = []
        self.start_purge_monitor()

    def start_purge_monitor(self):
        """Starts the timer that after the time period sends the batch of packets"""

        # Starts another thread
        self.throttle_job = threading.Timer(self.throttle_period, self.throttle_purge).start()

    def stop(self):
        """Stops the purge monitor job"""

        self.throttle_job.cancel()
        self.print('[!] Throttle purge job stopped!')