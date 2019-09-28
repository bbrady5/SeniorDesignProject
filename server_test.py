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


'''
#removing all images from image to send
            directory = "c:\\Faces\\Images_to_send"
            #coming from os.listdir() sorted alphabetically
            for filename in os.listdir(directory):
                if filename.endswith(".jpg"):
                    os.remove(directory + "\\" + filename)
                    #print("remove SUCCESS")
                    continue
                else:
                    print("ERROR2")
                    continue
'''


s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
print("about to bind")
s.bind((HOST, PORT))
print("about to listen")
s.listen(0)
print("listened")
# receive text file
conn, address = s.accept()
print(conn)
print(address)
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
conn.close()
s.close()
print("connection/connection closed")
print("text file closed.")
#read file and separate into list
f = open(filename, "r") #rb
lines = f.read().splitlines()
n=len(lines)
print("lines = "+ str(n))
print(lines)

print("about to declare")
# receive images
i=1
m=0
uos.chdir("/Rec_faces")

while m<n:
    print("entered while loop")
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    print("about to bind")
    PORT +=1
    print(PORT)
    s.bind((HOST, PORT))
    print("about to listen")
    s.listen(0)
    print("listened")

    conn, address = s.accept()
    print(conn)
    print(address)
    print("connection")
    filepicname= lines[m] #how does it know its a string?
    print(filepicname)
    f = open(filepicname, "wb") # renamed file
    print("opened file")
    while True:
        try:
            veri = conn.recv(2000)
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
    #conn.close()
    #print("connection closed")
    s.close()
    print("socket closed")
