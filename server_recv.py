

import requests
import json
from datetime import datetime
import threading
import os
import shutil
import socket
import time



print("~~~~~~~~~~~~~~~~SERVER_RECV~~~~~~~~~~~~~~~~~~~~~~")
#austin's computer
HOST='153.104.46.182'
PORT=8005
print(HOST)
print(PORT)

#os.chdir("/")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)
conn, address = s.accept()
print(address)

filename= "C:\\Camera_sim\\general_txt.txt"
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
    pass
else:
   
    with open('C:\\Camera_sim\\camfaces_txt.txt', 'w') as filetxt:
        for listitem in lines:
            filetxt.write('%s\n' % listitem)
        filetxt.close()
    
    PORT +=1
    print(PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(100)
    conn, address = s.accept()
    print(address)
    
    filename= "C:\\Camera_sim\\face_filesizes.txt"
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT +=1
        print(PORT)
        s.bind((HOST, PORT))
        s.listen(100)
        conn, address = s.accept()
        print(address)
    except Exception as e:
        print(e)
    #uos.chdir("/CamFaces")
    while m<n:
        filesize_str = filesizes[k]
        filesize = int(filesize_str)
        filepicname= lines[m]
        print(filepicname)
        f = open(filepicname, "wb")
        print("opened file")
        leave = None
        keep = None
        while(True):
            try:
                if leave is not None:
                    f.write(leave)
                veri = None
                leave = None
                veri = conn.recv(1)
                #print(len(veri))
                #f.write(veri)
            except Exception as e:
                print(e)
                print("no more bytes - received full image")
                break
            try:
                if ((filesize - len(veri)) < 0 ):
                    raise Exception
                else:
                    f.write(veri)
                    filesize -= len(veri)
                    veri = None
                #print("filesize:")
                #print(filesize)
            except Exception:
                print(filesize)
                keep = veri[:filesize]
                print(len(keep))
                leave = veri[filesize:]
                print(len(leave))
                f.write(keep)
                break
    
    
        f.close()
        print("picture written to file and closed.")
    
        i+=1
        m+=1
        k+=1
    conn.close()
    s.close()
    print("connection and socket closed")
    