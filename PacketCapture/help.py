
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
                                
Extra Optionals:

--target-packet, -tp    <packet-type>        
    * Only performs an affect on the specified packet type

--arp, -a               <victimIP> <routerIP> <interface>       
    * Performs arp spoofing with the passed parameters
    """

