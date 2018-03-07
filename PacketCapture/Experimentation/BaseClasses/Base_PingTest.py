import os
from BaseClasses.Base_Test import Base_Test
import subprocess


class PingTest(Base_Test):
    """Test that looks for the accuracy in the simulation of latency"""

    def __init__(self, filename, max_effect_value, start_effect_value, effect_step, repeat_tests, data_headers, max_test_time, print_time_estimate):
        super().__init__(filename,
                         max_effect_value=max_effect_value,
                         start_effect_value=start_effect_value,
                         effect_step=effect_step,
                         repeat_tests=repeat_tests,
                         data_headers=data_headers,
                         max_test_time=max_test_time,
                         print_time_estimate=print_time_estimate)

        self.NUMBER_OF_PINGS = 50
        self.INTERVAL = 0.2  # Min is 0.2

    def custom_test_behavior(self, effect_value, data):
        """To be overidden"""
        pass

    def grab_ping_value(self):
        """Runs a latency command as a subprocess and obtains a response string"""

        with open(os.devnull, 'w') as NULL:

            try:
                response = subprocess.check_output(
                                ['ping', '-c', str(self.NUMBER_OF_PINGS), '127.0.0.1', '-i', str(self.INTERVAL)],
                                stderr=NULL,
                                universal_newlines=True)
            except subprocess.CalledProcessError as e:
                self.force_print('Error:' + str(e))
                response = None

            if response is not None:
                return self.format_ping_output(response)

    def format_ping_output(self, ping_str):
        """Takes the output from a ping command and obtains the latency values"""

        lines = ping_str.split('\n')

        # Range starts at 1 to skip the first line
        # There are also 5 lines at the end that are not needed, that is why the range is the len() - 5
        ping_lines = []
        for x in range(1, len(lines) - 5):
            ping_lines.append(lines[x])

        ping_values = []
        for line in ping_lines:

            # Example line:
            #   e.g. '64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.079 ms'
            parts = line.split('=')
            latency_value = parts[-1]

            # The 'ms' string is now removed
            #
            #   e.g.  ' 0.013 ms'
            parts = latency_value.split(' ')
            latency_number = parts[0]

            # The last value is the latency of the ping
            ping_values.append(float(latency_number))

        return ping_values
