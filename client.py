#!/usr/bin/env python

import socket
import os


host='10.137.76.191'
port=8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

f = open("penguin1.jpg", "rb")

while True:

    veri = f.read(512)
    print("herefirst")
    if not veri:
        print("errhere1")
        break
    s.send(veri)
    print("512 bytes sent")

f.close()

print("picture sent?")

s.close()



'''
# host='127.0.0.1'
host='10.137.76.191'
port=8080

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

directory="/Users/BredaMarie/PycharmProjects/Test2_TCP/jpgpics/"
try:
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            print("here1")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("here1.2")
            s.connect((host, port))
            print(filename)
            filer = "/Users/BredaMarie/PycharmProjects/Test2_TCP/jpgpics/" + filename
            f = open(filer, "rb")
            print("here2")
            while True:

                veri = f.read(5120)
                if not veri:
                    break
                s.send(veri)

            f.close()
            print("picture sent")
            print("Success")
            s.close()
            print("here3")
            continue
        else:
            print("Error")
            continue
except Exception as e:
    print(e)
    print("error collecting files")






while True:

    veri = f.read(512)
    if not veri:
        break
    s.send(veri)

f.close()

print("picture sent")

#s.close()

'''