Main logic: 
    1. Bring down the network adapter 
    2. Change the MAC
    3. Bring the adapter online
    4. Verify the change

Requirements for the code to execute successfully: 
    - Python
    - Unix OS
    - ifconfig tool 

Steps followed by code: 
    ifconfig {interface} down
    ifconfig {interface} hw ether {new_mac}
    ifconfig {interface} up

Arguments accepted by tool: 
    -i or --interface 
        Interface whose MAC is to be changed
    -m or --mac 
        New MAC address