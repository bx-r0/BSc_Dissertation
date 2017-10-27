## This iptable command needs to be run to push all packets into the NFQUEUE
#----------------------------------------#
# "sudo iptables -A INPUT -j NFQUEUE"
#----------------------------------------#

from netfilterqueue import NetfilterQueue

def print_packet(packet):
    print("[!] ", end='')
    print(packet)

# Creates the object
nfqueue = NetfilterQueue()

# 0 is the default NFQUEUE and print_packet is the
nfqueue.bind(0, print_packet)

try:
    print("[*] Waiting ")
    nfqueue.run()
except KeyboardInterrupt:
    pass