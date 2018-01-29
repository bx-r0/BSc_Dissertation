from scapy.all import *


data = 'University of Texas at San Antonio'
a = IP(dst='127.0.0.1') / UDP() / Raw(load=data)
sendp(a)
