# TCP Client Example
#
# This example shows how to send and receive TCP traffic with the WiFi shield.

import network, usocket

# AP info
SSID='Villanova Senior Design' # Network SSID
KEY='merakipassword'  # Network key

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")

wlan = network.WINC()
print(" here 1.00")
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
print(" here 1.0")
# We should have a valid IP now via DHCP
print(wlan.ifconfig())
print(" here 1.1")
# Get addr info via DNS
addr = usocket.getaddrinfo("www.google.com", 80)[0][4]
print(" here 1.2")
# Create a new socket and connect to addr
client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
client.connect(addr)
print(" here 2")
# Set timeout to 1s
client.settimeout(1.0)
print(" here 3")
# Send HTTP request and recv response
client.send("GET / HTTP/1.0\r\n\r\n")
print(client.recv(1024))
print(" here 4")
# Close socket
client.close()
print(" here 5")
