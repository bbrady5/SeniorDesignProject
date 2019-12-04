import sensor, image, time, network, usocket, sys, uos, pyb, gc
def server_recv():
    print("~~~~~~~~~~~~~~~~SERVER_RECV~~~~~~~~~~~~~~~~~~~~~~")
    HOST=configure[0]
    PORT=8005
    print(HOST)
    print(PORT)
    pyb.LED(2).on()
    uos.chdir("/")
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(100)
    conn, address = s.accept()
    print(address)
    begin_time = pyb.millis()
    print("begin time in server_recv:", begin_time)
    filename= "general_txt.txt"
    f = open(filename, "wb")
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
    f = open(filename, "r")
    lines = f.read().splitlines()
    n=len(lines)
    print("lines = "+ str(n))
    print(lines)
    f.close()
    nochange = []
    nochange.append('no change')
    if nochange[0] == lines[1]:
        end_time1 = pyb.elapsed_millis(begin_time)
        print("end time1 in server_recv:", end_time1)
        send_time1 = 150000 - end_time1
        print("send time1 in server_recv:", send_time1)
        pyb.LED(2).off()
        return send_time1, lines[0]
    else:
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
        with open('camfaces_txt.txt', 'w') as filetxt:
            for listitem in lines:
                filetxt.write('%s\n' % listitem)
            filetxt.close()

        PORT +=1
        print(PORT)
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(100)
        conn, address = s.accept()
        print(address)

        filename= "face_filesizes.txt"
        f = open(filename, "wb")
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
        print("connection closed - face filesize file closed")
        f = open(filename, "r")
        filesizes = f.read().splitlines()
        r=len(filesizes)
        print("filesizes = "+ str(r))
        print(filesizes)
        f.close()





        i=1
        m=1
        k=0
        try:
            s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
            PORT +=1
            print(PORT)
            s.bind((HOST, PORT))
            s.listen(100)
            conn, address = s.accept()
            print(address)
        except Exception as e:
            print(e)
        uos.chdir("/CamFaces")
        while m<n:
            filesize_str = filesizes[k]
            filesize = int(filesize_str)
            filepicname= lines[m]
            print(filepicname)
            f = open(filepicname, "wb")
            print("opened file")
            while(filesize > 0):
                try:
                    veri = conn.recv(1)
                    #print(len(veri))
                    f.write(veri)
                    filesize -= len(veri)
                except Exception as e:
                    print(e)
                    print("no more bytes - received full image")
                    break



            f.close()
            print("picture written to file and closed.")

            i+=1
            m+=1
            k+=1
        conn.close()
        s.close()
        print("connection and socket closed")
        pyb.LED(2).off()
        end_time2 = pyb.elapsed_millis(begin_time)
        print("end time2 in server_recv:", end_time2)
        send_time2 = 150000 - end_time2
        print("send time2 in server_recv:", send_time2)
        gc.collect()
        return send_time2, lines[0]
def face_detect(init_start, calc_time):
    print("~~~~~~~~~~~~~~~~FACE_DETECT~~~~~~~~~~~~~~~~~~~~~~")
    gc.collect()
    while pyb.elapsed_millis(init_start) < calc_time:
        RED_LED_PIN = 1
        BLUE_LED_PIN = 3
        sensor.reset()
        sensor.set_contrast(3)
        sensor.set_gainceiling(16)
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.HQVGA)
        sensor.skip_frames(time = 2000)
        face_cascade = image.HaarCascade("frontalface", stages=25)
        uos.chdir("/")
        pyb.LED(RED_LED_PIN).on()
        print("About to start detecting faces...")
        sensor.skip_frames(time = 2000)
        pyb.LED(RED_LED_PIN).off()
        print("Now detecting faces!")
        pyb.LED(BLUE_LED_PIN).on()
        diff = 10
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
                    elif (pyb.elapsed_millis(init_start)) > calc_time:
                        raise Exception
            pyb.LED(BLUE_LED_PIN).off()
            print("Face detected! Saving image...")
            pic_name = "snapshot-person.pgm"
            sensor.snapshot().save(pic_name)
            pyb.delay(100)
            gc.collect()
            return pic_name
        except Exception as go:
            print("exception - time expired")
            pyb.LED(BLUE_LED_PIN).off()
            gc.collect()
def face_recog(pic_name, vi_ip):
    print("~~~~~~~~~~~~~~~~FACE_RECOG~~~~~~~~~~~~~~~~~~~~~~")
    gc.collect()
    snap_img = image.Image(pic_name, copy_to_fb=True).mask_ellipse()
    d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
    pyb.LED(2).on()
    pyb.LED(3).on()
    name_lbp_list = []
    uos.chdir("/CamFaces")
    for filename in uos.listdir("/CamFaces"):
        if filename.endswith(".pgm") :
            try:
                img = None
                img = image.Image(filename, copy_to_fb=True).mask_ellipse()
                sensor.alloc_extra_fb(img.width(), img.height(), sensor.GRAYSCALE)
                d1 = img.find_lbp((0, 0, img.width(), img.height()))
                dist = image.match_descriptor(d0, d1,50)
                sensor.dealloc_extra_fb()
                pname = filename
                und_loc = pname.index('_')
                pname = pname[0:(und_loc)]
                name_lbp_list.append(pname)
                name_lbp_list.append(dist)
                continue
            except Exception as e:
                print(e)
                print("error producing LBP value")
        else:
            print("file found that is not of type pgm")
    print(name_lbp_list)
    gc.collect()
    end = 0
    name_avg = []
    i = 0
    start = 0
    while i < len(name_lbp_list):
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
    gc.collect()
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
    gc.collect()
    min_lbp = min(lbps)
    print(min_lbp)
    ind = lbps.index(min(lbps))
    ind += 1
    found_person = name_avg[2*ind - 2]
    id_name = "The person you are looking at is: " + found_person
    print(id_name)
    uos.remove("/snapshot-person.pgm")
    pyb.LED(2).off()
    pyb.LED(3).off()
    chost = vi_ip
    cport = 8080
    client = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    client.connect((chost,cport))
    print("connected to visually impaired user's smartphone")
    to_send = id_name + "\n"
    client.send(to_send.encode())
    print("sent name to phone")
    client.close()
    gc.collect()
    return
SSID='Villanova Senior Design - wirele'
KEY='merakipassword'
#SSID='VUPlay'
#KEY='vuplay123'
while(True):
    print("Trying to connect... (may take a while)...")
    wlan = network.WINC()
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
    configure = wlan.ifconfig()
    print(configure)
    if(configure[0] != '0.0.0.0'):
        break
while(True):
    calc_time, vi_ip = server_recv()
    gc.collect()
    init_start = pyb.millis()
    while pyb.elapsed_millis(init_start) < calc_time:
        pic_name = face_detect(init_start, calc_time)
        gc.collect()
        if (pyb.elapsed_millis(init_start)) < calc_time:
            face_recog(pic_name, vi_ip)
    gc.collect()
