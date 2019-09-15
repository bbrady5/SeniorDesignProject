#!/usr/bin/env python

import socket

host='127.0.0.1'
port=5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(1)

sock, address = s.accept()
print("connection")

def recvall(baglanti, buf):

# baglanti  means connection in turkish
    data = ""
    while len(data) < buf:
        packet = baglanti.recv(buf - len(data))
        if not packet:
            return None
        data += packet
    return data

f = open("pic_here.png", "w") # renamed file

while True:

    veri = sock.recv(512)
    if not veri:
        break
    f.write(veri)
f.close()
print("picture received.")
sock.close()

s.close()