
import requests
import json
from datetime import datetime
import threading
import os
import shutil
import socket
import time



previous_list = []
current_list = []

def capture():
    global previous_list
    global current_list
    
    print("Current Date and Time of Run:")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Camera WiFi MAC address =  f8:f0:05:a1:b9:df
    # to figure out which Meraki device the camera is connected to:
    url = "https://api.meraki.com/api/v0/networks/L_634444597505819269/clients/f8:f0:05:a1:b9:df"
    
    headers = {
        'X-Cisco-Meraki-API-Key': "b70ca858020930863c1542f511ec4267ab077aa6",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "0ca6880f-406a-46a4-8431-5e72757386be,e60c1ffd-fde9-42c6-8268-6443ff63f554",
        'Accept-Encoding': "gzip, deflate",
        'Referer': "https://api.meraki.com/api/v0/networks/L_634444597505819269/clients/f8:f0:05:a1:b9:df",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    
    response = requests.request("GET", url, headers=headers)
    
    print(response.text)
    json_data0 = json.loads(response.text)
    recentDeviceMac = json_data0["recentDeviceMac"]
    print(recentDeviceMac)   
        
    
    #for the Meraki device which the camera is connected to, find that device's serial number
    url = "https://api.meraki.com/api/v0/networks/L_634444597505819269/devices"
    
    headers = {
        'X-Cisco-Meraki-API-Key': "b70ca858020930863c1542f511ec4267ab077aa6",
        'cache-control': "no-cache",
        'Postman-Token': "9a429afd-9a2b-4bf3-84b9-8e70ba4c475f"
        }
    
    response = requests.request("GET", url, headers=headers)
    
    print(response.text)
    json_data1 = json.loads(response.text)
    for item in json_data1: 
        mac = item.get("mac")
        if mac == recentDeviceMac :
            serial = item.get("serial")
            print(serial)
    
    #list all clients connected to device with matching serial number
    url = "https://api.meraki.com/api/v0/devices/" + serial + "/clients" #Q2PD-6WK9-V4XS for MR33, Q2XD-4RAF-S592 for MR20
    
    querystring = {"timespan":"20000"} # check what clients were connected to the Meraki in the past (timespan) seconds - set to past 5 minutes (300 seconds)
    
    headers = {
        'X-Cisco-Meraki-API-Key': "b70ca858020930863c1542f511ec4267ab077aa6",
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "338b5785-52d9-412e-9db4-ea90361e0e69,441570a6-a644-42cb-8446-9244f803d755",
        'accept-encoding': "gzip, deflate",
        'referer': "https://api.meraki.com/api/v0/devices/Q2PD-6WK9-V4XS/clients?timespan=86400",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    print("JSON Results:")
    print(response.text)
    json_data = json.loads(response.text)
    
    if len(json_data) != 0: # if the JSON is not empty:
        #open a text file to write the names of people (clients) connected to AP
        first_file_path = "C:\\Faces\\Images_to_send\\face_txt.txt"
        first_file = open(first_file_path, "w")
        #empty the file of any previous contents
        first_file.seek(0)
        first_file.truncate()
        print("Client Names found:")
        for item in json_data: #isolating name (description) from other client info
            desc = item.get("description")
            directory = "c:\\Faces\\" + desc
            vi_ip = '153.104.46.181'
            host = '10.137.69.21'
            if desc == "WINC-b9-df": # if client is the camera, get its IP address
                host = item.get("ip")
                print("camera ip address: " + host)
                continue
            elif desc == "V_I_User": # if client is the visually impaired user's smartphone, get its IP address
                vi_ip = item.get("ip")
                print("visually impaired user's device ip address: " + vi_ip)
                continue
            else: #otherwise add the names of the clients to the current list of connected clients
                print(desc)
                #current_list.append(desc)
                #moving selected images to a different folder to be sent to camera
                try:
                    
                    for filename in sorted(os.listdir(directory)):
                        
                        if filename.endswith(".pgm"):
                            #current_list.append(desc)
                            pathname = "C:\\Faces\\" + desc + "\\" + filename
                            shutil.copy(pathname, "C:\\Faces\\Images_to_send")
                            first_file.write(filename + "\n")
                        else:
                            print("file found that is not of type pgm")
                            continue
                    current_list.append(desc)
                except Exception as e: #if there is not a corresponding folder in Faces, then we assume the client is not a coworker's smartphone - ignoring
                    print(e)
                    print("Stationary device - ignoring")
        first_file.close()
        #alphabetize the text file of names
        alphalist = []
        first_file_path = "C:\\Faces\\Images_to_send\\face_txt.txt"
        with open(first_file_path) as first:
            for line in first:
                alphalist.append(line)
        first.close()
        alphalist.sort()
        with open(first_file_path, 'w') as fout:
            fout.write(vi_ip + "\n") #include the visually impaired user's smartphone's IP address as first line in text file
            for alpha in alphalist:
                fout.write(alpha)
        fout.close()
        #compare lists to see if there have been any changes since the last time the code was run
        print("previous list:")
        print(previous_list)
        print("current list:")
        print(current_list)
        if previous_list == current_list: 
            print ("The lists are identical..no need to send new photos to the camera") 
            client_nochange(host, vi_ip) #call to TCP function to tell camera no need to get new photos
        else : 
            print ("The lists are not identical..refreshing camera with new photos")
            client_send(host) # call to TCP function to tell camera that we are sending it new photos
            
            #removing all old images from Images_to_send in order to start fresh next time the code is run
            directory = "c:\\Faces\\Images_to_send"
            for filename in os.listdir(directory):
                if filename.endswith(".pgm"):
                    os.remove(directory + "\\" + filename)
                    continue
                else:
                    print("no more files in directory to delete")
                    continue
                
        previous_list = current_list.copy() #now make the current list the previous list for the next time the code is run      
        current_list.clear() #clear the current list to start fresh the next time
        
        
        
        
        
        
        
    
def client_send(host_ip): #TCP Client function to send new photos
    host = host_ip # camera's IP address
    print(host)
    port=8005 
    
    #here sending a text file containing image names
    try:
        time.sleep(6)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create TCP socket with IPv4 addressing
        #s.connect((host, port)) # connect to camera's IP address at port 8005
        connected = False
        while (connected == False):
            try:
                s.connect((host, port)) # connect to camera's IP address at the next available sequential port number
                connected = True
            except Exception as f:
                print(f)
                time.sleep(3)
        print("waiting for camera...")
        #recv1 = s.recv(512) #receive a message from the camera stating that it is ready to receive data
        #print(recv1)
        textfile = "C:\\Faces\\Images_to_send\\face_txt.txt"
        f = open(textfile, "rb")
        while True:
            veri = f.read(512)
            if not veri:
                print("finished sending file - no more bytes to send")
                break
            s.send(veri) #send data 512 bytes at a time
        f.close()
        s.close()
        print("text file sent")
    
    except Exception as e:
        print(e)
        print("Error3 - error with sending text file")
    
    #~~~~~~~~~~~~~~~sending filesizes
    # here sending multiple images
    
    
    directory="C:\Faces\Images_to_send"
    os.chdir(directory)
    image_size_path = "C:\\Faces\\Images_to_send\\face_sizes.txt"
    image_size_file = open(image_size_path, "w")
    directory="C:\Faces\Images_to_send"
    try:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".pgm"): #for each image in Images_to_send:
                print(filename)
                filesize = os.path.getsize(filename)
                print(filesize)
                image_size_file.write(str(filesize) + "\n")
                continue
            else:
                print("Error 4 - error collecting image")
                continue
    except Exception as e:
        print(e)
        print("Error 5 - cannot find image")
    image_size_file.close()
    
    try:
        time.sleep(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create TCP socket with IPv4 addressing
        port += 1
        print(port)
        connected = False
        while (connected == False):
            try:
                s.connect((host, port)) # connect to camera's IP address at the next available sequential port number
                connected = True
            except Exception as f:
                print(f)
                time.sleep(3)
        print("waiting for camera...")

        f = open(image_size_path, "rb")
        while True:
            veri = f.read(512)
            if not veri:
                print("finished sending file - no more bytes to send")
                break
            s.send(veri) #send data 512 bytes at a time
        f.close()
        s.close()
        print("file size text file sent")
    
    except Exception as e:
        print(e)
        print("Error3 - error with sending text file")
    
    #~~~~~~~~~~~~~~~sending ~~~~~~~~~~~~~~~images in one socket
    # here sending multiple images
    time.sleep(6)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create TCP socket with IPv4 addressing
    port += 1
    print(port)
    connected = False
    while (connected == False):
        try:
            s.connect((host, port)) # connect to camera's IP address at the next available sequential port number
            connected = True
        except Exception as f:
            print(f)
            time.sleep(3)
    
    directory="C:\Faces\Images_to_send"
    try:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".pgm"): #for each image in Images_to_send:
                print(filename)
                filer = "C:\\Faces\\Images_to_send\\" + filename
                f = open(filer, "rb")
                while True:
                    veri = f.read(512)
                    if not veri:
                        print("finished sending image - no more bytes to send")
                        break
                    s.send(veri) #send data 512 bytes at a time
                f.close()
                
                continue
            else:
                print("Error 4 - error collecting image")
                continue
        s.close()
    except Exception as e:
        print(e)
        print("Error 5 - error sending image")

def client_nochange(host_ip, vi_ip): #TCP Client function to send new photos
    host = host_ip # camera's IP address
    print(host)
    port=8005
    
    #here sending a string to the camera to say no change in clients have occurred 
    try:
        time.sleep(6)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create TCP socket with IPv4 addressing
        #s.connect((host, port)) # connect to camera's IP address at port 8005
        connected = False
        while (connected == False):
            try:
                s.connect((host, port)) # connect to camera's IP address at the next available sequential port number
                connected = True
            except Exception as f:
                print(f)
                time.sleep(3)
        #recv2 = s.recv(512) #receive a message from the camera stating that it is ready to receive data
        #print(recv2)
        nochange = "\nno change"
        s.send((vi_ip + nochange).encode()) #send camera the visually impaired user's smartphone's IP address (in case of change), followed by 'no change'
        s.close()
        print("no change text sent")
    
    except Exception as e:
        print(e)
        print("Error3 - error with sending no change text")
    

def timed_prog():
    threading.Timer(180.0, timed_prog).start() # run program every 300 seconds - 5 minutes
    capture()
    print("----------------------")
    
timed_prog() #main function call

