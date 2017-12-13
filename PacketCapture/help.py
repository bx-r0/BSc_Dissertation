
def Usage():
    return"""
Effects:
--print, -p                                  Prints all the packets
--display-bandwidth, -b                      Displays information on the transfer rate
      
--latency, -l       <delay>(ms)              Applies latency on the connection   
--packet-loss, -pl  <loss percentage>(%)     Performs packet loss on the connection
--throttle, -t      <delay>(ms)              Throttles the connection by the given delay 
--duplicate, -d     <factor>                 Duplicates a packet by the specified factor
--combination, -c   <latency> <packet-loss>  Performs latency and packet loss at the same time
--simulate, -s      <connection_name>        Simulates real world connections e.g. 3G
--rate-limit, -rl   <rate> (B/s)             Limits the throughput of the program
                                
Extra Optionals:
--target-packet, -tp    <packet-type>        Only performs an affect on the specified packet type

--arp, -a               <victimIP> <routerIP> <interface>       
                                             Performs arp spoofing with the passed parameters
    """

