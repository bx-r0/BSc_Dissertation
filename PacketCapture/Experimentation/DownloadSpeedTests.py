# Speed test code is not included on the repo due to it not being created by me:
# It can be downloaded here:
#       https://github.com/sivel/speedtest-cli
#
# I've changed it slightly to include the method "get_all()" this just returns the value of the download
# And upload
import os
import speedtest as speed
import subprocess
import time
import sys


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

    PROCESS = subprocess.Popen(cmd, stdout=open('log.txt', 'w'))


def grab_speeds():
    """Talks to the speedtest.py script to grab upload and download speeds"""

    print('[*] Speed test starting!')

    global DOWNLOAD, UPLOAD

    download, upload = speed.get_all()

    download_speed_in_Mbps = download / 1000000
    upload_speed_in_Mbps = upload / 1000000

    DOWNLOAD = download_speed_in_Mbps
    UPLOAD = upload_speed_in_Mbps


def print_speeds(download, upload):
    print(' ' * 50, end='\r')
    print("\n[!] ### Download: {:.2f}Mbps - Upload: {:.2f}Mbps ### [!]\n".format(download, upload))

try:

    # Grabs all the parameters
    # Note: No validation
    parameters = sys.argv[1:]

    # Removes the arguments so the speed script doesn't take them as well
    del sys.argv[1:]

    # No parameters defaults as just a connection speed tets
    if len(parameters) > 1:
        run_degradation_script(parameters)
    else:
        print('[*] Just testing network speeds')

    grab_speeds()
    clean_close('', '')

    # Waits for all other messages to come through
    time.sleep(0.5)

    print_speeds(DOWNLOAD, UPLOAD)
    sys.exit(0)

except Exception as e:
    print('Error', e)
