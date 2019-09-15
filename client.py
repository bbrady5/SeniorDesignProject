#!/usr/bin/env python

import socket

host='127.0.0.1'
port=5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host , port))

f = open("../pic_c.png", "rb")

while True:

    veri = f.read(512)
    if not veri:
        break
    s.send(veri)

f.close()

print("picture sent?")

s.close()