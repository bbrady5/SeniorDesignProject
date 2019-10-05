'''
Created on Aug 4, 2019

@author: Brady
'''

import requests
import json
from datetime import datetime
import threading
import os
import shutil
import socket
import time


url = "https://api.meraki.com/api/v0/devices/Q2PD-6WK9-V4XS/clients"

querystring = {"timespan":"1000600"} # change time to 15

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

previous_list = []
current_list = []


def capture():
    global previous_list
    global current_list
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("Current Date and Time of Run:")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("JSON Results:")
    print(response.text)
    
    json_data = json.loads(response.text)
    if len(json_data) != 0: # if the JSON is not empty
        #open a text file to write the names of people connected to AP
        first_file_path = "C:\\Faces\\Images_to_send\\face_txt.txt"
        first_file = open(first_file_path, "w")
        #empty the file of any previous contents
        first_file.seek(0)
        first_file.truncate()
        print("Client Names found:")
        for item in json_data: #isolating name from other device info
            desc = item.get("description")
            directory = "c:\\Faces\\" + desc
            #print(directory)
            if desc == "WINC-b9-df":
                #host = item.get("ip")
                #print("camera ip address: " + host)
                continue
            else:
                print(desc)
                current_list.append(desc)
                # moving selected images to a different folder to be sent to camera
                try:
                    for filename in sorted(os.listdir(directory)):
                        if filename.endswith(".pgm"):
                            pathname = "C:\\Faces\\" + desc + "\\" + filename
                            shutil.copy(pathname, "C:\\Faces\\Images_to_send")
                            first_file.write(filename + "\n")
                            
                        else:
                            print("ERROR")
                            continue
                except Exception as e:
                    print(e)
                    print("Stationary device - ignoring")
        first_file.close()
        #alphabetize the file of names
        alphalist = []
        first_file_path = "C:\\Faces\\Images_to_send\\face_txt.txt"
        with open(first_file_path) as first:
            for line in first:
                alphalist.append(line)
        first.close()
        alphalist.sort()
        with open(first_file_path, 'w') as fout:
            for alpha in alphalist:
                fout.write(alpha)
        fout.close()
        #print("face text file sorted")
        
        if previous_list == current_list: 
            print ("The lists are identical..no need to refresh camera") 
        else : 
            print ("The lists are not identical..refreshing camera with new photos")
            # call to TCP server function to send photos
            host='10.132.78.207'
            server_send(host)
            #removing all images from image to send
            directory = "c:\\Faces\\Images_to_send"
            for filename in os.listdir(directory):
                if filename.endswith(".pgm"):
                    os.remove(directory + "\\" + filename)
                    continue
                else:
                    print("no more files in directory to delete")
                    continue
        previous_list = current_list
        current_list.clear()
   
    
    

def timed_prog():
    threading.Timer(30.0, timed_prog).start() # run program every 30 seconds
    capture()
    print("----------------------")
    

def server_send(host_ip): #TCP Server function
    host= host_ip
    print(host)
    port=8005
    
    #here sending a text file containing picture names
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        textfile = "C:\\Faces\\Images_to_send\\face_txt.txt"
        f = open(textfile, "rb")
        while True:
            veri = f.read(512)
            if not veri:
                print("finished sending file - no more bytes to send")
                break
            s.send(veri)
        f.close()
        s.close()
        print("text file sent")
    
    except Exception as e:
        print(e)
        print("Error3 - error with sending text file")
    
    # here sending multiple images
    directory="C:\Faces\Images_to_send"
    try:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".pgm"):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port += 1
                print(port)
                s.connect((host, port))
                print(filename)
                filer = "C:\\Faces\\Images_to_send\\" + filename
                f = open(filer, "rb")
                while True:
    
                    veri = f.read(512)
                    print(len(veri))
                    if not veri:
                        print("finished sending image - no more bytes to send")
                        break
                    s.send(veri)
                f.close()
                s.close()
                time.sleep(3)
                continue
            else:
                print("Error 4 - error collecting image")
                continue
    except Exception as e:
        print(e)
        print("Error 5 - error sending image")


    
    
timed_prog()


# need to handle exceptions for when a device does not have a photo in faces folder