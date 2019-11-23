# Untitled - By: Brady - Wed Nov 20 2019

import sensor, image, time, network, usocket, sys, uos, pyb, gc


def server_recv():
    print("~~~~~~~~~~~~~~~~SERVER_RECV~~~~~~~~~~~~~~~~~~~~~~")
    HOST=configure[0] #host is the IP address assigned to the camera's WiFi shield
    PORT=8005
    print(HOST)
    print(PORT)
    pyb.LED(2).on() #green light while in server mode
    uos.chdir("/")
    #get general text file from computer
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #TCP server socket with IPv4 addressing
    s.bind((HOST, PORT))
    s.listen(100) #listen for connection requests - backlog up to 100
    conn, address = s.accept() #accept connection request from computer
    print(address)
    begin_time = pyb.millis() #start timer
    print("begin time in server_recv:", begin_time)
    filename= "general_txt.txt"
    f = open(filename, "wb")
    print("opened file")
    conn.send("camera ready to start receiving data...")
    while True:
        try:
            veri = conn.recv(512) #receive 512 bytes at a time
            f.write(veri) #write data to text file
        except Exception as e:
            print(e)
            print("no more bytes - finished receiving text file")
            break
    f.close()
    conn.close()
    s.close()
    print("connection closed - text file closed")

    #determine if need to new faces or not:
    #read file and separate into list
    f = open(filename, "r") #rb
    lines = f.read().splitlines()
    n=len(lines)
    print("lines = "+ str(n))
    print(lines)
    f.close()
    nochange = []
    nochange.append('no change')
    if nochange[0] == lines[1]: #if the computer sent 'no change' to the camera:
        end_time1 = pyb.elapsed_millis(begin_time) #stop timer
        print("end time1 in server_recv:", end_time1)
        #4.5 minutes = 270000 millis
        send_time1 = 270000 - end_time1
        print("send time1 in server_recv:", send_time1)
        pyb.LED(2).off() #turn off green light
        return send_time1, lines[0]
    else: #else the computer is about to send new photos to refresh the camera with:
        #delete any old photos in the CamFaces directory
        uos.chdir("/CamFaces")
        directory = "/CamFaces"
        for filename in uos.listdir(directory):
            if filename.endswith(".pgm"):
                uos.remove(directory + "/" + filename)
                continue
            else:
                print("file found not of type pgm")
                continue
        print("deleted all old photos")
        uos.chdir("/")
        #copy face names to new file
        with open('camfaces_txt.txt', 'w') as filetxt:
            for listitem in lines:
                filetxt.write('%s\n' % listitem)
            filetxt.close()
        #receive images
        i=1
        m=1
        uos.chdir("/CamFaces")
        while m<n: #loop for number of images to be received
            try:
                s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #TCP server socket with IPv4 addressing
                PORT +=1 #use next available sequential port number
                print(PORT)
                s.bind((HOST, PORT))
                s.listen(100) #listen for connection requests - backlog up to 100
                conn, address = s.accept() #accept connection request from computer
                print(address)
            except Exception as e:
                print(e)
            filepicname= lines[m] #set current image file name to the corresponding name received in text file
            print(filepicname)
            f = open(filepicname, "wb")
            print("opened file")
            s.settimeout(2.0) # 2 second timeout on blocking socket operations
            while True:
                try:
                    veri = conn.recv(512) #receive image data
                    f.write(veri)
                except Exception as e:
                    print(e)
                    print("no more bytes - received full image")
                    break
            f.close()
            print("picture written to file and closed.")
            conn.close()
            s.close()
            print("connection and socket closed")
            i+=1
            m+=1
        pyb.LED(2).off() #turn off green light
        end_time2 = pyb.elapsed_millis(begin_time) #stop timer
        print("end time2 in server_recv:", end_time2)
        #4.5 minutes = 270000 millis
        send_time2 = 270000 - end_time2
        print("send time2 in server_recv:", send_time2)
        gc.collect() #garbage collection
        return send_time2, lines[0]


def face_detect(init_start, calc_time):
    print("~~~~~~~~~~~~~~~~FACE_DETECT~~~~~~~~~~~~~~~~~~~~~~")
    gc.collect() #garbage collection
    while pyb.elapsed_millis(init_start) < calc_time: #while time not expired
        #snapshot on face detection
        RED_LED_PIN = 1
        BLUE_LED_PIN = 3
        sensor.reset() # Initialize the camera sensor.
        sensor.set_contrast(3) #set to highest contrast setting
        sensor.set_gainceiling(16)
        sensor.set_pixformat(sensor.GRAYSCALE) #grayscale for facial recognition
        sensor.set_framesize(sensor.HQVGA)
        sensor.skip_frames(time = 2000) # Let new settings take affect.
        face_cascade = image.HaarCascade("frontalface", stages=25) #Using Frontal Face Haar Cascade Classifier
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
                    sensor.alloc_extra_fb(img.width(), img.height(), sensor.GRAYSCALE) #allocate more space for image
                    faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5) #detecting face features
                    sensor.dealloc_extra_fb()
                    if faces:
                        diff -= 1
                        for r in faces:
                            img.draw_rectangle(r)
                    elif (pyb.elapsed_millis(init_start)) > calc_time: #if time is expired, leave function
                        raise Exception
            pyb.LED(BLUE_LED_PIN).off()
            print("Face detected! Saving image...")
            pic_name = "snapshot-person.pgm"
            sensor.snapshot().save(pic_name) # Save Pic. to root of SD card
            pyb.delay(100)
            gc.collect() #garbage collection
            return pic_name
        except Exception as go:
            print("exception - time expired")
            pyb.LED(BLUE_LED_PIN).off()
            gc.collect() #garbage collection


def face_recog(pic_name, vi_ip):
    print("~~~~~~~~~~~~~~~~FACE_RECOG~~~~~~~~~~~~~~~~~~~~~~")
    gc.collect() #garbage collection
    #find LBP value for snapshot saved in face_detect
    snap_img = image.Image(pic_name, copy_to_fb=True).mask_ellipse()
    d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
    # turn on lights signaling facial recognition calculations starting
    pyb.LED(2).on()
    pyb.LED(3).on()
    #find LBP values for each image received in server_recv
    name_lbp_list = []
    uos.chdir("/CamFaces") # change directory to where all the images from server_recv are stored
    for filename in uos.listdir("/CamFaces"):
        if filename.endswith(".pgm") :
            try:
                img = None
                img = image.Image(filename, copy_to_fb=True).mask_ellipse()
                sensor.alloc_extra_fb(img.width(), img.height(), sensor.GRAYSCALE) #allocate more space for images
                d1 = img.find_lbp((0, 0, img.width(), img.height()))
                dist = image.match_descriptor(d0, d1,50) #set threshold lower than 70 to tighten matching algo
                sensor.dealloc_extra_fb()
                # extracting the person's name from the file name
                pname = filename
                und_loc = pname.index('_')
                pname = pname[0:(und_loc)]
                # add the person's name and LBP value for the image to the list
                name_lbp_list.append(word)
                name_lbp_list.append(dist)
                continue
            except Exception as e:
                print(e)
                print("error producing LBP value")
        else:
            print("file found that is not of type pgm")
    print(name_lbp_list)
    gc.collect() #garbage collection
    # finding average LBP values for each name
    end = 0
    name_avg = []
    i = 0
    start = 0
    while i < len(name_lbp_list): # for names 1 thru n-1
        if ( (i+2) < len(name_lbp_list)) and (name_lbp_list[i] != name_lbp_list[i+2] ) :
            end = i+2
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
    gc.collect() #garbage collection
    # special case: find average LBP value for last name in list (name n)
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
    gc.collect() #garbage collection
    # find minimum average LBP and associated person name
    min_lbp = min(lbps)
    print(min_lbp)
    ind = lbps.index(min(lbps))
    ind += 1
    found_person = name_avg[2*ind - 2]
    id_name = "The person you are looking at is: " + found_person
    print(id_name)
    #delete snapshot of person
    uos.remove("/snapshot-person.pgm")
    # turn off lights signaling facial recognition calculations done
    pyb.LED(2).off()
    pyb.LED(3).off()
    #TCP client socket to send name of the person recognized to the visually impaired user's smartphone
    chost = vi_ip
    cport = 8080
    client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #TCP client socket with IPv4 addressing
    client.connect((chost,cport))
    print("connected to visually impaired user's smartphone")
    to_send = id_name + "\n"
    client.send(to_send.encode())
    print("sent name to phone")
    client.close() #client closed
    gc.collect() #garbage collection
    return


# AP info
SSID='Villanova Senior Design - wirele' # Network SSID
KEY='merakipassword'  # Network key


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


while(True): #main loop
    calc_time, vi_ip = server_recv()
    gc.collect() #garbage collection
    init_start = pyb.millis()
    while pyb.elapsed_millis(init_start) < calc_time: #while time has not expired:
        pic_name = face_detect(init_start, calc_time)
        gc.collect() #garbage collection
        if (pyb.elapsed_millis(init_start)) < calc_time: #if time has still not expired
            face_recog(pic_name, vi_ip)
    gc.collect() #garbage collection

