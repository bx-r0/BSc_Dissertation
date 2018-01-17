"""Changes made here will effect the parameters taken for each effect"""

cmd_latency = '-l'
cmd_packetloss = '-pl'
cmd_target_packet = '-tp'
cmd_print = '-p'
cmd_bandwidth = '-b'
cmd_throttle = '-t'
cmd_duplicate = '-d'
cmd_simulate = '-s'
cmd_ratelimit = '-rl'
cmd_combination = '-c'
cmd_outoforder = '-o'
cmd_arp = '-a'
cmd_save = '-sa'
cmd_graph = '-g'


def Usage():
    return"""
Effects:
--print, -p                                  
    * Prints all the packets
    
--display-bandwidth, -b                     
    * Displays information on the transfer rate
      
--latency, -l <delay_ms>            
    * Applies latency on the connection   
    
--packet-loss, -pl  <loss_percentage>  
    * Performs packet loss on the connection

--throttle, -t      <delay_ms> 
    * Throttles the connection by the given delay 
    
--duplicate, -d     <factor>                 
    * Duplicates a packet by the specified factor

--simulate, -s      <connection_name>        
    * Simulates real world connections e.g. 3G
    
--rate-limit, -rl   <rate_bytes>            
    * Limits the throughput of the program
                                
--combination, -c   <latency_ms> <packet-loss> <bandwidth_bytes>
    * Performs latency and packet loss at the same time
    
--out-of-order, -o 
    * Sets the mode to out of order that alters the order of incoming packets
                                
Extra Optionals:

--target-packet, -tp    <packet-type>        
    * Only performs an affect on the specified packet type

--arp, -a               <victimIP> <routerIP> <interface>       
    * Performs arp spoofing with the passed parameters
    
--save, -s
    * Tells the program to start saving all the packets that run through the system
    
--graph, -g             <chart_type>
    * Sets the program in graph mode where it collates information to create a graph
    
    ## Chart_Types ##
        
        All-Modes:
        
            0 -     Will show a bar graph with the total number of a packets' 
                    protocol that the script has collected
                
            10 -    Will process a line graph with number of packets over time
            
        Latency:
        
            1 - TODO
            
        Packet Loss:
        
            1 - Will show the packet loss percentage over time
            2 - Shows total packets lost over time
            
        Bandwidth:
        
            1 - Will show the rate of transfer over time
    """

