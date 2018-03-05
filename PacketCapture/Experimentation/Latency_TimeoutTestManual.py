import subprocess

cmd = 'sudo python ../Packet.py -l 100'
list_cmd = cmd.split(' ')

wget_cmd = 'wget -q ftp://speedtest.tele2.net/512KB.zip'
list_wget = wget_cmd.split(' ')

wget_thread = None
script_thread = None

try:
    script_thread = subprocess.Popen(list_cmd)
    print("Packet Script PID: " + script_thread.pid)

    wget_thread = subprocess.Popen(list_wget)

    wget_thread.wait()
    script_thread.kill()

except:

    if wget_thread != None:
        wget_thread.kill()

    if script_thread != None:
        script_thread.kill()



