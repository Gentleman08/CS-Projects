import scapy.all as scapy
import argparse

interface = scapy.conf.iface

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range to scan")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify target address to scan.")
    return options

def scan(dst_ip, src_mac):
    arp_request = scapy.ARP(pdst=dst_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff", src=src_mac)
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)

    return client_list

def print_result(result_list):
    print("\n+-----------------------------------------------+")
    print("|     IP\t\t|   MAC Address\t\t|")
    print("+-----------------------------------------------+")
    for client in result_list:
        print("| " + client["ip"]+ "\t\t|   " + client["mac"] + "\t|")

    print("|_______________________________________________|\n\n")

options = get_arguments()
scan_result = scan(options.target, scapy.conf.iface.mac)
print_result(scan_result)