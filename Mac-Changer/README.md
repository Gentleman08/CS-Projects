Main logic: 
    1. Generate an ARP request with target IP 
    2. Generate Ethernet frame with destination MAC set to Broadcast 
    3. Combine Ethernet frame with ARP request
    4. Send the Ethernet frame in the LAN
    5. Recive response 
    6. Fetch IP and MAC from the response

Requirements for the code to execute successfully: 
    - Python
    - scapy 

Arguments accepted by tool: 
    -t or --target 
        Target IP / IP range to scan