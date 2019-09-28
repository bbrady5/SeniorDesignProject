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
#from nntplib import first

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
    #global host
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("Current Date and Time of Run:")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("JSON Results:")
    print(response.text)
    
    json_data = json.loads(response.text)
    if len(json_data) != 0:
        first_file_path = "C:\\Faces\\Images_to_send\\face_txt.txt"
        first_file = open(first_file_path, "w")
        #empty the file of its contents
        first_file.seek(0)
        first_file.truncate()
        #count = 0
        print("Client Names found:")
        for item in json_data:
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
                
                try:
                    for filename in sorted(os.listdir(directory)):
                        if filename.endswith(".jpg"):
                            #print("about to copy to images_to_send..") 
                            pathname = "c:\\Faces\\" + desc + "\\" + filename
                            shutil.copy(pathname, "c:\\Faces\\Images_to_send")
                            #print("copy SUCCESS")
                            first_file.write(filename + "\n")
                            #count += 1
                            #continue
                        else:
                            print("ERROR")
                            continue
                except Exception as e:
                    print(e)
                    print("Stationary device - ignoring")
        #first_file.write(str(count))
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
        #sorted(first_file.readlines())
        #first_file.close()
        print("face text file sorted")
        
        if previous_list == current_list: 
            print ("The lists are identical..no need to refresh camera") 
        else : 
            print ("The lists are not identical..refreshing camera with new photos")
            host='10.137.76.191'
            server_send(host)
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
        previous_list = current_list
        current_list.clear()
   
    
    

def timed_prog():
    threading.Timer(30.0, timed_prog).start() # called every 15 seconds
    capture()
    print("----------------------")
    

def server_send(host_ip): 
    host= host_ip
    print(host)
    port=8005
    
    #here sending a text file containing count and pic names
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("here1.2")
        s.connect((host, port))
        
        textfile = "C:\\Faces\\Images_to_send\\face_txt.txt"
        f = open(textfile, "rb")
        #print("here2")
        while True:
            veri = f.read(512)
            #print("herefirst")
            if not veri:
                print("errhere1")
                break
            s.send(veri)
            print("text sent sent")
        f.close()
        s.close()
        print("file and socket closed for text")
    
    except Exception as e:
        print(e)
        print("error3 collecting files")
    
    # here sending multiple images
    directory="C:\Faces\Images_to_send"
    try:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".jpg"):
                print("here1")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("here1.2")
                port += 1
                print(port)
                s.connect((host, port))
                print(filename)
                filer = "C:\\Faces\\Images_to_send\\" + filename
                f = open(filer, "rb")
                print("here2")
                while True:
    
                    veri = f.read(2000)
                    print("herefirst")
                    if not veri:
                        print("errhere1")
                        break
                    s.send(veri)
                    print("512 bytes sent")
                f.close()
                s.close()
                print("picture sent")
                print("Success")
                print("here3")
                continue
            else:
                print("Error")
                continue
    except Exception as e:
        print(e)
        print("error collecting files")
    #s.close()


    
    
timed_prog()

# add a refresh function to send updated names to camera
# need to handle exceptions for when a device does not have a photo in faces folder