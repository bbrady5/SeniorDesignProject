# Cam_script - By: Brady - Sat Sep 7 2019
import sensor, image, time, network, usocket, sys, uos, pyb


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
    time.sleep(100)



#snapshot on face detection
RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

face_cascade = image.HaarCascade("frontalface", stages=25)

# while(True): --- loop whole program //at end

pyb.LED(RED_LED_PIN).on()
print("About to start detecting faces...")
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
print("Now detecting faces!")
pyb.LED(BLUE_LED_PIN).on()

diff = 10 # We'll say we detected a face after 10 frames.
while(diff):
        img = sensor.snapshot()
        faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

        if faces:
            diff -= 1
            for r in faces:
                img.draw_rectangle(r)

pyb.LED(BLUE_LED_PIN).off()
print("Face detected! Saving image...")
pic_name = "snapshot-new.pgm" # add %d, make a count each time it goes through the loop
sensor.snapshot().save(pic_name) # Save Pic.


#uos.chdir("/")
snap_img = image.Image(pic_name).mask_ellipse()
d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
# face recognition
'''
NUM_SUBJECTS = 5
NUM_SUBJECTS_IMGS = 10

img = image.Image(pic_name).mask_ellipse()
d0 = img.find_lbp((0, 0, img.width(), img.height()))
img = None

print("")
for s in range(1, NUM_SUBJECTS+1):
    dist = 0
    for i in range(2, NUM_SUBJECTS_IMGS+1):
        img = image.Image("orl_faces/s%d/%d.pgm"%(s, i)).mask_ellipse()
        d1 = img.find_lbp((0, 0, img.width(), img.height()))
        dist += image.match_descriptor(d0, d1)
    print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
'''
lbp_list = []
name_list = []

uos.chdir("/Faces")
for filename in uos.listdir("/Faces"):
  if filename.endswith(".pgm") :
    img = None
    img = image.Image(filename).mask_ellipse()
    d1 = img.find_lbp((0, 0, img.width(), img.height()))
    dist = image.match_descriptor(d0, d1)
    lbp_list.append(dist)
    word = filename
    und_loc = word.index('_')
    word = word[0:(und_loc)]

    #print(word)
    name_list.append(word)


    #print("Success")
    continue
  else:
    print("ERROR")

#print(lbp_list)
#print(name_list)

list_set = set(name_list)
# convert the set to the list
unique_list = (list(list_set))
unique_list.reverse()
res = [name_list.index(i) for i in unique_list]

# print result
'''
print("The Match indices list is : " + str(res))
print()
print("name list")
print(name_list)
print()
print("lbp list")
print(lbp_list)
print("unique list")
print(unique_list)

print(res)
'''

i = 0
x=0


total = 0
i = 0
lbp_unique_list = []
while i < (len(res)-1):
    start = res[i]
    end = res[i+1]
    i+= 1
    j = start
    count = 0
    while j < end :
        total += lbp_list[j]
        j+= 1
        count += 1
    lbp_avg = total/count
    #print(lbp_avg)
    lbp_unique_list.append(lbp_avg)

    total = 0
    count = 0

last = end

while last  < len(lbp_list):
    total += lbp_list[last]
    last+= 1
    count += 1
lbp_avg = total/count
#print(lbp_avg)
lbp_unique_list.append(lbp_avg)
print(lbp_unique_list)
print(min(lbp_unique_list))
name_ind = lbp_unique_list.index(min(lbp_unique_list))
print(name_ind)
print(unique_list[name_ind])
id_name = "The person you are looking at is: " + unique_list[name_ind]
print(id_name)


#set up client connection to phone

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host2
#port2
c.connect((host2, port2))
try:
    c.send((idname).encode())
    print("face id text sent")
except Exception as e:
    print(e)
    print("error sending face id string")
c.close()


