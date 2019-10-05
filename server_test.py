# Untitled - By: Brady - Mon Sep 16 2019
import sensor, image, time, network, usocket, sys, uos

# AP info
SSID='VUPlay' # Network SSID
KEY='vuplay123'  # Network key
#SSID='Villanova Senior Design - wirele' # Network SSID
#KEY='merakipassword'  # Network key

HOST=''
PORT=8005


while True:
    # Init wlan module and connect to network
    print("Trying to connect... (may take a while)...")

    wlan = network.WINC()
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

    # We should have a valid IP now via DHCP
    configure = wlan.ifconfig()
    print(configure)
    #retry if get an invalid IP address
    if(configure[4] != '0.0.0.0'):
        break


s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(20)
# receive text file
conn, address = s.accept()
print(conn)
print(address)
filename= "faces_txt.txt"
f = open(filename, "wb") # renamed file
print("opened file")
while True:
    try:
        veri = conn.recv(512)
        f.write(veri)
    except Exception as e:
        print(e)
        print("no more bytes - finished receiving text file")
        break

f.close()
conn.close()
s.close()
print("connection closed - text file closed")

#read file and separate into list
f = open(filename, "r") #rb
lines = f.read().splitlines()
n=len(lines)
print("lines = "+ str(n))
print(lines)

# receive images
i=1
m=0
uos.chdir("/Faces")

#delete any old photos in this directory

directory = "/Faces"
for filename in uos.listdir(directory):
    if filename.endswith(".pgm"):
        uos.remove(directory + "/" + filename)
        continue
    else:
        print("no more files in directory to delete")
        continue



while m<n: #loop for number of images to be received
    try:
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        PORT +=1
        print(PORT)
        s.bind((HOST, PORT))
        s.listen(20)
        conn, address = s.accept()
        print(address)
    except Exception as e:
        print(e)
    filepicname= lines[m]
    print(filepicname)
    f = open(filepicname, "wb") # renamed file
    print("opened file")
    while True:
        try:
            veri = conn.recv(512)
            print(len(veri))
            f.write(veri)
        except Exception as e:
            print(e)
            print("no more bytes - received full image")
            break

    f.close()
    print("picture written to file and closed.")
    i+=1
    m+=1
    conn.close()
    print("connection closed")
    s.close()
    print("socket closed")

