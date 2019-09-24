# Untitled - By: Brady - Mon Sep 16 2019
import sensor, image, time, network, usocket, sys

# AP info
SSID='Villanova Senior Design - wirele' # Network SSID
KEY='merakipassword'  # Network key

HOST='10.102.31.94'
PORT=8000

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")

wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

# We should have a valid IP now via DHCP
print(wlan.ifconfig())

s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
print("about to bind")
s.bind((HOST, PORT))
print("about to listen")
s.listen(1)
print("listened")
# receive text file
conn, address = s.accept()
print("connection")
filename= "faces_txt.txt"
f = open(filename, "wb") # renamed file
print("opened file")
while True:
    try:
        veri = conn.recv(512)
        print("received face bytes")
        f.write(veri)
        print("text written to file")
    except Exception as e:
        print(e)
        print("no more bytes")
        break

f.close()
print("text file closed.")
#read file and separate into list
f = open(filename, "r") #rb
lines = f.read().splitlines()
n=len(lines)

print("about to declare")
# receive images
i=1
m=0
while m<n:
    print("entered while loop")
    conn, address = s.accept()
    print("connection")
    filepicname= lines[m] #how does it know its a string?
    f = open(filepicname, "wb") # renamed file
    print("opened file")
    while True:
        try:
            veri = conn.recv(512)
            print("received 512 bytes")
            f.write(veri)
            print("picture written to file")
        except Exception as e:
            print(e)
            print("no more bytes")
            break

    f.close()
    print("picture closed.")
    i+=1
    m+=1

conn.close()
print("connection closed")
s.close()
print("socket closed")
