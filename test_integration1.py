# Untitled - By: Brady - Mon Nov 4 2019

import sensor, image, time, network, usocket, sys, uos, pyb


# AP info
#SSID='VUPlay' # Network SSID
#KEY='vuplay123'  # Network key
SSID='Villanova Senior Design - wirele' # Network SSID
KEY='merakipassword'  # Network key



#assumption time
#time = 90000 -- 1.5---3.5 minutes in millis
while(True):
    # Init wlan module and connect to network
    print("Trying to connect... (may take a while)...")

    wlan = network.WINC()
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

    # We should have a valid IP now via DHCP
    configure = wlan.ifconfig()
    print(configure)
    #retry if get an invalid IP address
    if(configure[0] != '0.0.0.0'):
        break


'''
pin = pyb.millis()
print(pin)
cc = 0
#pyb.elapsed_millis(start)
while pyb.elapsed_millis(pin) < calc_time:
'''
print("top of face recog function")
#snapshot on face detection
RED_LED_PIN = 1
BLUE_LED_PIN = 3
sensor.reset() # Initialize the camera sensor.
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
face_cascade = image.HaarCascade("frontalface", stages=25)
uos.chdir("/")
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
pic_name = "snapshot-person.pgm"
sensor.snapshot().save(pic_name) # Save Pic. to root of SD card -- uos.chdir("/")
pyb.delay(100)
snap_img = image.Image(pic_name).mask_ellipse()
d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
# face recognition
pyb.LED(2).on()
name_lbp_list = []
uos.chdir("/Faces") # change directory to where all the webex photos from tcp are stored
for filename in uos.listdir("/Faces"):
    if filename.endswith(".pgm") :
        try:
            img = None
            img = image.Image(filename).mask_ellipse()
            d1 = img.find_lbp((0, 0, img.width(), img.height()))
            dist = image.match_descriptor(d0, d1,50)
            print("weve matched")
            word = filename
            #print(filename)
            und_loc = word.index('_')
            word = word[0:(und_loc)]
            name_lbp_list.append(word)
            name_lbp_list.append(dist)
            continue
        except Exception as e:
            print(e)
            print("error reading file")
    else:
        print("ERROR")
print(name_lbp_list)
#print(len(name_lbp_list))
end = 0
name_avg = []
i = 0
start = 0
while i < len(name_lbp_list):
    if ( (i+2) < len(name_lbp_list)) and (name_lbp_list[i] != name_lbp_list[i+2] ) :
        end = i+2
        #print(start)
        #print(end)
        face = []
        face = name_lbp_list[start:end]
        print(face)
        j = 1
        sum_lbp = 0
        while j < len(face):
            sum_lbp += face[j]
            j += 2
        name_avg.append(face[0])
        name_avg.append(sum_lbp/(len(face)/2))
        start = i+2
    i += 2
face = []
face = name_lbp_list[(end):(len(name_lbp_list))]
print(face)
j = 1
sum_lbp = 0
while j < len(face):
    sum_lbp += face[j]
    j += 2
name_avg.append(face[0])
name_avg.append(sum_lbp/(len(face)/2))
print(name_avg)
lbps = []
k = 1
while k < len(name_avg):
    lbps.append(name_avg[k])
    k +=2
print(lbps)
#print(len(lbps))
min_lbp = min(lbps)
print(min_lbp)
ind = lbps.index(min(lbps))
#print(ind)
ind += 1
found_person = name_avg[2*ind - 2]
id_name = "The person you are looking at is: " + found_person
print(id_name)
#delete snapshot of person
uos.remove("/snapshot-person.pgm")
pyb.LED(2).off()

#client socket
chost = "153.104.47.149"
cport = 5000
client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
client.connect((chost,cport))
to_send = id_name + "\n"
# Send HTTP request and recv response
client.send(to_send.encode())
#client.send(b'herenow')
# Close socket
client.close()

