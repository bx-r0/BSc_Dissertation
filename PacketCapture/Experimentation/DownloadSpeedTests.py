# Speed test code is not included on the repo due to it not being created by me:
# It can be downloaded here:
#       https://github.com/sivel/speedtest-cli
#
# I've changed it slightly to include the method "get_all()" this just returns the value of the download
# And upload
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import speedtest as speed
import subprocess
import time
import csv
from Terminal import Terminal

FILE_NAME = 'LatencyDownloadSpeed.csv'


"""The script is run by passing:

        <effect_parameter> <effect_value_start><hyphen><effect_value_end><hyphen><effect_step>"""

# Translates parameter to effect and unit
Parameter_values = \
    [
        ["-l", "Latency", "ms"],
        ["-pl", "Packet Loss", "%"],
        ["-rl", "Bandwidth", "B/s"]
    ]


def clean_close(signum, frame):
    """Used to kill the packet script process and close the script down nicely"""

    try:
        os.system('pkexec kill -SIGINT {}'.format(PROCESS.pid))
        print('[*] Process closed!')
    except Exception as e:
        print('[!] Error in clean_close():', e)


def run_degradation_script(parameters):
    """This runs the packets script with custom parameters in the background
    while the speed test is performed"""

    global PROCESS
    PROCESS = None

    start_time = time.time()

    print('[*] Running degradation script')

    script_name = "/Packet.py"

    # Filepath code
    filepath = os.path.dirname(os.path.abspath(__file__))

    # Moves back a directory
    directories = filepath.split('/')
    del directories[-1]

    # Joins the values back up but seperated by a '/'
    filepath = "/".join(directories)

    cmd = ['python', (filepath + script_name)]

    # Adds on the parameters
    for x in parameters:
        cmd.append(x)

    PROCESS = subprocess.Popen(cmd, stdout=open(os.devnull, 'w'))
    print("PROCESS PID: ", PROCESS.pid)

    # Speed code
    grab_speeds()

    end_time = time.time()

    elapsed_time = end_time - start_time

    print('[!] Test complete - Elapsed Time: {:.2f} seconds'.format(elapsed_time))
    PROCESS.terminate()


def grab_speeds():
    """Talks to the speedtest.py script to grab upload and download speeds"""

    print('[*] Speed test starting!')

    global DOWNLOAD, UPLOAD

    download, upload = speed.get_all()

    download_speed_in_Mbps = download / 1000000
    upload_speed_in_Mbps = upload / 1000000

    DOWNLOAD = download_speed_in_Mbps
    UPLOAD = upload_speed_in_Mbps


def print_speeds():
    Terminal.clear_line()
    print("[!] Download: {:.2f}Mbps - Upload: {:.2f}Mbps".format(DOWNLOAD, UPLOAD))


def save_csv():

    # Saves the data
    with open(FILE_NAME, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(effect_values)
        writer.writerow(download_values)
        writer.writerow(upload_values)


def get_parameters():
    # Grabs all the parameters
    # Note: No validation
    parameters = sys.argv[1:]

    if len(parameters) > 1:

        values = parameters[1:]

        possible_range_value = values[-1].split('-')

        # If it is a range parameter
        if len(possible_range_value) > 1:

            #   Format:
            #       <start> <dash> <end> <dash> <step>
            #   e.g.
            #       10 - 100 - 2

            # Nicer naming
            range_values = possible_range_value

            new_range = range(int(range_values[0]), int(range_values[1]), int(range_values[2]))

            parameters.append(new_range)

            return parameters
        # If it's a regular parameter
        else:
            return parameters

    # No parameters defaults as just a connection speed test
    else:
        print('[*] Just testing network speeds')
        return None


def multiple_tests(parameters):

    global download_values, upload_values, effect_values, effect_parameter_flag

    effect_parameter_flag = parameters[0]
    download_values = ["Download"]
    upload_values = ["Upload"]
    effect_values = []

    # Translates parameters into units and names dynamically
    effect_name = ''
    effect_unit = ''
    for x in Parameter_values:
        if x[0] == effect_parameter_flag:
            effect_name = x[1]
            effect_unit = x[2]
    effect_values.insert(0, effect_name)

    range_of_values = parameters[-1]
    print('[*] Tests will be performed on this range: \'{}\''.format(range_of_values))

    # Zero effect value
    # Grabs zero effect value
    grab_speeds()
    print_speeds()

    # Saves data to a series of lists
    effect_values.append(str(0) + " " + effect_unit)
    download_values.append(str(round(DOWNLOAD, 5)))
    upload_values.append(str(round(UPLOAD, 5)))

    for value in range_of_values:
        test = [parameters[0], str(value)]

        print('\n[!] New test - Type: \'{}\' - Effect level: \'{}\''.format(test[0], test[1]))

        run_degradation_script(test)

        # Saves data to a series of lists
        effect_values.append(str(value) + " " + effect_unit)
        download_values.append(str(round(DOWNLOAD, 5)))
        upload_values.append(str(round(UPLOAD, 5)))

        print('[!] Data saved!')
        save_csv()
        print_speeds()

        # Saves and closes the previous script
        clean_close('', '')


parameters = get_parameters()
del sys.argv[1:]  # Stop other scripts from grabbing already used parameters

if parameters is not None:

    try:
        # Range parameters
        if isinstance(parameters[-1], range):
            print('[!] Multiple test mode activated!')
            multiple_tests(parameters)

        # If the parameters are regular
        else:
            run_degradation_script(parameters)

            time.sleep(0.5)
            print_speeds()
    except:
        if PROCESS is not None:
            PROCESS.terminate()

else:
    grab_speeds()
    print_speeds()