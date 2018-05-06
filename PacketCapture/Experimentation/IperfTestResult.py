import re
import subprocess


class TestResult:
    """
    Class that encases IPEF functionality into an object

    Dictionary Options
    ------------------
    Interval
    Transfer
    Bandwidth
    Write
    Err
    Rtry
    Cwnd
    RTT
    """

    def __init__(self, update_interval=0, test_time=10, address='127.0.0.1'):
        """
        Bandwidth and Transfer are measured in :
                MB (Transfer)
                Mb/sec (Bandwidth)
        :param test_time: - Length of the test (default: 10)
        """

        self.CMD = "sudo iperf -c {} -t {} -f m".format(address, test_time)

        if update_interval > 0:
            self.CMD += ' -i {}'.format(update_interval)

        # Single tests
        self.retransmissions = None
        self.bandwidth = None
        self.total_transferred = None

        # For multi tests
        self.results_dict = {}

    def run_test(self):
        """
        Basic test that returns a raw output
        :return:
        """
        start_retransmission = TestResult.get_current_retransmission_value()

        # # # Runs script
        server = subprocess.Popen('iperf -s', shell=True, stdout=subprocess.DEVNULL)
        output = subprocess.check_output(self.CMD.split(' '))
        server.kill()

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

        self.extract_stats_update(self.run_test())

    def add_value_to_dictionary(self, key, value):
        if key not in self.results_dict:
            self.results_dict[key] = [value]
        else:
            value_list = self.results_dict[key]
            value_list.append(value)
            self.results_dict[key] = value_list

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
        bandwidth = speed_line_values[-2].strip()
        transfer = speed_line_values[-4].strip()

        return float(bandwidth), float(transfer)

    def extract_stats_update(self, output):
        """
        Extracts stats from an update line that is specified with the -i option
        :param output: Entire output from the script
        """

        lines = bytes(output).decode('utf-8').split('\n')

        # Removes the first 6 lines and the final line
        for i in range(0, len(lines) - 1):
            if i < 6:
                del lines[0]

        lines = [row for row in lines if not row.startswith('[ ID]') and not row == '']

        # Extracts values from all the lines
        for x in range(0, len(lines) - 2):
            line_values = (TestResult.extract_stats_line(lines[x]))

            for values in line_values:
                self.add_value_to_dictionary(values[0], values[1])

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

        # Removes the front section
        output = re.sub(r'\[.*\]', '', str(output)).strip()

        # Splits by gaps
        parts = re.split(r'( ){2,}', output)

        # Removes blank values
        parts = [x for x in parts if x.strip() is not '']

        # # Regular mode
        # -------------------------------------------------#
        # [ ID] Interval       Transfer     Bandwidth
        # '0.0- 0.6 sec', '29.0 MBytes', '405 Mbits/sec'
        # -------------------------------------------------#
        if len(parts) is 3:
            interval_part = parts[0]
            time_range = re.findall(float_regex, interval_part)


            transfer_part = parts[1]
            transferred = re.findall(float_regex, transfer_part)[0]

            bandwidth_part = parts[2]
            bandwidth = re.findall(r'\d+', bandwidth_part)[0]

            # time_range returns the end time
            return \
            [
                ['Interval', time_range[1]],
                ['Transfer', transferred],
                ['Bandwidth', bandwidth]
            ]

        # # Precise mode
        # -------------------------------------------------------------------------------- #
        # [ ID] Interval        Transfer    Bandwidth       Write/Err  Rtry    Cwnd/RTT
        # ['0.00-0.40 sec', '19.0 MBytes', '398 Mbits/sec', '152/0',   '45', '831K/8272 us']
        # -------------------------------------------------------------------------------- #
        elif len(parts) is 6:
            interval_part = parts[0]
            time_range = re.findall(float_regex, interval_part)

            # TODO: Errors occurring here when transfer is too high
            transferred = None
            try:
                transfer_part = parts[1]
                transferred_parts = re.findall(float_regex, transfer_part)

                if transfer_part is None:
                    transferred = re.findall(r'\d+', transfer_part)[0]
                else:
                    transferred = transferred_parts[0]

            except:
                print('Error: ', transfer_part)

            bandwidth_part = parts[2]
            bandwidth = re.findall(r'\d+', bandwidth_part)[0]

            write_error_part = parts[3]
            write_error_split = write_error_part.split('/')
            write = write_error_split[0]
            error = write_error_split[1]

            retry_part = parts[4]

            cwnd_rtt_part = parts[5]
            cwnd_rtt_split = cwnd_rtt_part.split('/')

            congestion_window = cwnd_rtt_split[0]
            congestion_window = re.sub(r'K', '', congestion_window)
            round_trip_time = cwnd_rtt_split[1]

            return \
            [
                ['Interval', time_range[1]],
                ['Transfer', transferred],
                ['Bandwidth', bandwidth],
                ['Write', write],
                ['Err', error],
                ['Rtry', retry_part],
                ['Cwnd', congestion_window],
                ['RTT', round_trip_time.split(' ')[0]]
            ]
        else:
            print('Error: extract_stats_line() invalid line format' )
            return None

        # Returns:
        #   End Time, Transferred and Bandwidth

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

