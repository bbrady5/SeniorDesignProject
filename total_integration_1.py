# Untitled - By: Brady - Thu Nov 7 2019

import sensor, image, time, network, usocket, sys, uos, pyb, gc

def facial_recog(pic_name, vi_ip):
    cc=0
    snap_img = image.Image(pic_name, copy_to_fb=True).mask_ellipse()
    d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
    # face recognition
    pyb.LED(2).on()
    name_lbp_list = []
    uos.chdir("/Faces") # change directory to where all the webex photos from tcp are stored
    for filename in uos.listdir("/Faces"):
        if filename.endswith(".pgm") :
            try:
                img = None
                img = image.Image(filename, copy_to_fb=True).mask_ellipse()
                sensor.alloc_extra_fb(img.width(), img.height(), sensor.GRAYSCALE)
                d1 = img.find_lbp((0, 0, img.width(), img.height()))
                dist = image.match_descriptor(d0, d1,50)
                sensor.dealloc_extra_fb()
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
            print("file found that is not of type pgm")
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
    cc += 1
    print(cc)
    #client socket
    chost = vi_ip
    print(chost)
    #chost = "10.132.30.198"
    cport = 8080
    client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    client.connect((chost,cport))
    print("connected to android")
    to_send = id_name + "\n"
    # Send HTTP request and recv response
    client.send(to_send.encode())
    # Close socket
    client.close()
    gc.collect()

def face_recog(calc_time, vi_ip):
    pin = pyb.millis()
    print(pin)
    print(calc_time)
    cc = 0
    #pyb.elapsed_millis(start)
    while pyb.elapsed_millis(pin) < calc_time:
        print("top of face recog function")
        #snapshot on face detection
        RED_LED_PIN = 1
        BLUE_LED_PIN = 3
        sensor.reset() # Initialize the camera sensor.
        sensor.set_contrast(3)
        sensor.set_gainceiling(16)
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.HQVGA) # or sensor.QQVGA (or others)
        #sensor.alloc_extra_fb()
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
        try:
            while(diff):
                    img = sensor.snapshot()
                    sensor.alloc_extra_fb(img.width(), img.height(), sensor.GRAYSCALE)
                    faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)
                    sensor.dealloc_extra_fb()
                    if faces:
                        diff -= 1
                        for r in faces:
                            img.draw_rectangle(r)
                    elif (pyb.elapsed_millis(pin)) > calc_time:
                        raise Exception
            pyb.LED(BLUE_LED_PIN).off()
            print("Face detected! Saving image...")
            pic_name = "snapshot-person.pgm"
            sensor.snapshot().save(pic_name) # Save Pic. to root of SD card -- uos.chdir("/")
            pyb.delay(100)
            facial_recog(pic_name, vi_ip)
            gc.collect()
        except Exception as go:
            print("we are in exception")
            pyb.LED(BLUE_LED_PIN).off()
            gc.collect()

def server_recv():
    HOST=''
    PORT=8005
    begin_time = pyb.millis()
    pyb.LED(2).on()
    uos.chdir("/")
    #get general text file
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(40)
    # receive text file
    conn, address = s.accept()
    print(conn)
    print(address)
    filename= "general_txt.txt"
    f = open(filename, "wb") # renamed file
    print("opened file")
    conn.send("camera ready to start receiving data...")
    while True:
        try:
            veri = conn.recv(512)
            f.write(veri)
        except Exception as e:
            print(e)
            print("no more bytes - finished receiving text file")
            break

    #conn.send("camera done receiving data...")
    f.close()
    conn.close()
    s.close()
    print("connection closed - text file closed")

    #determine if new faces or not



    #read file and separate into list
    f = open(filename, "r") #rb
    lines = f.read().splitlines()
    n=len(lines)
    print("lines = "+ str(n))
    print(lines)
    f.close()
    nochange = []
    nochange.append('no change')
    if nochange == lines[1]:
        end_time1 = pyb.elapsed_millis(begin_time)
        #4.5 minutes = 270000 millis
        send_time1 = 150000 - end_time1
        face_recog(send_time1, lines[0])
    else:

        #delete any old photos in this directory
        uos.chdir("/Faces")
        directory = "/Faces"
        for filename in uos.listdir(directory):
            if filename.endswith(".pgm"):
                uos.remove(directory + "/" + filename)
                continue
            else:
                print("no more files in directory to delete")
                continue

        print("deleted old photos")
        uos.chdir("/")
        #copy face names to new file
        with open('faces_txt.txt', 'w') as filehandle:
            for listitem in lines:
                filehandle.write('%s\n' % listitem)
            filehandle.close()
        '''
        filename= "faces_txt.txt"
        f = open(filename, "wb") # renamed file
        print("opened file")
        f.write(lines)#change
        f.close()
        '''

        # receive images
        i=1
        m=1
        uos.chdir("/Faces")
        #receive loop
        while m<n: #loop for number of images to be received
            try:
                s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
                PORT +=1
                print(PORT)
                s.bind((HOST, PORT))
                s.listen(40)
                conn, address = s.accept()
                print(address)
            except Exception as e:
                print(e)
            filepicname= lines[m]
            print(filepicname)
            f = open(filepicname, "wb") # renamed file
            print("opened file")
            #conn.send("camera ready to start receiving data...")
            s.settimeout(2.0)
            while True:
                try:
                    veri = conn.recv(512)
                    #print(len(veri))
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
        pyb.LED(2).off()
        #st_time = (m + 20)*1000
        end_time2 = pyb.elapsed_millis(begin_time)
        #4.5 minutes = 270000 millis
        send_time2 = 150000 - end_time2
        face_recog(send_time2, lines[0])
        gc.collect()





# AP info
SSID='VUPlay' # Network SSID
KEY='vuplay123'  # Network key
#SSID='Villanova Senior Design - wirele' # Network SSID
#KEY='merakipassword'  # Network key



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

while(True):
    server_recv()
    gc.collect()
