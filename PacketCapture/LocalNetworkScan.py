import nmap
import socket
import queue

result = queue.Queue()

def scan_for_active_hosts():
    print('[!] Grabbing active hosts on your network')

    def grab_internal_ip():
        """This works by connecting with Google's DNS and grabbing the connection IP"""

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

        # Takes of the last octive
        ip = '.'.join(ip.split('.')[:3])

        return ip

    try:
        nm = nmap.PortScanner()
        ip_range = grab_internal_ip() + '.1-255'
        nm.scan(hosts=ip_range, arguments='-sP')

        active_hosts = []
        for x in nm.all_hosts():
            # Saves all the active hosts
            if nm[x].state() == 'up':
                active_hosts.append(x)

        result.put(active_hosts)
       # return active_hosts

    except KeyboardInterrupt:
        print('[!] Local scan canceled')

