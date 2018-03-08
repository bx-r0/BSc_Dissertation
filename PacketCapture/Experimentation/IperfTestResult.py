import re
import subprocess


class TestResult:

    def __init__(self, test_time=10):
        """
        Bandwidth and Transfer are measured in :
                MB (Transfer)
                Mb/sec (Bandwidth)
        :param test_time: - Length of the test (default: 10)
        """

        self.CMD = "sudo iperf -c 127.0.0.1 -t {} -f m".format(test_time)

        self.retransmissions = None
        self.bandwidth = None
        self.total_transferred = None

    def run_test(self):
        """
        Runs the iperf test. The retransmission values are also calculated here
        """

        start_retransmission = TestResult.get_current_retransmission_value()

        # # # Runs script
        output = subprocess.check_output(self.CMD.split(' '))

        # Calculates Retransmissions
        end_retransmission = TestResult.get_current_retransmission_value()
        self.retransmissions = end_retransmission - start_retransmission

        # Gets stats from the output
        self.bandwidth, self.total_transferred = self.extract_stats(output)

    @staticmethod
    def extract_stats(output):
        """
        Takes the download and transfer rate from the output string
        :return:
        """
        output_lines = bytes(output).decode('utf-8').split('\n')
        speed_line_parts = output_lines[-2].split(' ')
        speed_line_values = list(filter(lambda item: str(item) != "", speed_line_parts))

        # Grabs from the specific positions
        bandwidth = speed_line_values[-4].strip()
        transfer = speed_line_parts[-2].strip()

        return float(bandwidth), float(transfer)

    @staticmethod
    def get_current_retransmission_value():
        """
        Grabs the current retransmission value by querying netstat
        :return: Current retransmission value
        """
        # Runs the command
        cmd = "netstat -s | grep -i ret"
        retr = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # Finds all the values in the string
        value = map(int, re.findall(r'\d+', retr))

        # Adds up all the values
        total = 0
        for x in value:
            total += x

        return total



