import re
import subprocess


class TestResult:

    # TODO: Need to add server instance per test

    def __init__(self, update_interval=0, test_time=5):
        """
        Bandwidth and Transfer are measured in :
                MB (Transfer)
                Mb/sec (Bandwidth)
        :param test_time: - Length of the test (default: 10)
        """

        self.CMD = "sudo iperf -c 127.0.0.1 -t {} -f m -i {}".format(test_time, update_interval)

        self.retransmissions = None
        self.bandwidth = None
        self.total_transferred = None

        self.multi_results_list = []

    def run_test(self):
        """
        Basic test that returns a raw output
        :return:
        """
        start_retransmission = TestResult.get_current_retransmission_value()

        # # # Runs script
        output = subprocess.check_output(self.CMD.split(' '))

        # Calculates Retransmissions
        end_retransmission = TestResult.get_current_retransmission_value()
        self.retransmissions = end_retransmission - start_retransmission

        return output

    def run_single_test(self):
        """
        Runs the iperf test. The retransmission values are also calculated here
        """
        self.bandwidth, self.total_transferred = self.extract_stats(self.run_test())

    def run_multi_test(self):
        """
        Processes the result of an iperf with a multiple output set
        :return:
        """

        result = self.extract_stats_update(self.run_test())

        if result is not None:
            self.multi_results_list.append(result)

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
    def extract_stats_update(output):
        lines = bytes(output).decode('utf-8').split('\n')

        #TODO: Can't seem to delete last element of the list??

        # Removes the first 6 lines and the final line
        for i in range(0, 6):
            del lines[0]

        results = []

        # Extracts values from all the lines
        for x in range(0, len(lines) - 2):
            results.append(TestResult.extract_stats_line(lines[x]))

        return results

    @staticmethod
    def extract_stats_line(output):
        """
        Format:
            [ID] [Time Period] [Transfer]    [Bandwidth]
        e.g.
            [ 3] 0.0- 1.0 sec   3.68 GBBytes  31.7 Gbits/sec
        :param output:
        :return:
        """

        float_regex = r'\d+\.\d+'

        parts = str(output).split('  ')

        if len(parts) > 4:
            interval_part = parts[2]
            time_range = re.findall(float_regex, interval_part)

            transfer_part = parts[3]
            transferred = re.findall(float_regex, transfer_part)[0]

            bandwidth_part = parts[4]

            bandwidth = re.findall(r'\d+', bandwidth_part)[0]
        else:
            return None

        # Returns:
        #   End Time, Transferred and Bandwidth
        return [time_range[1], transferred, bandwidth]

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

