#!/usr/bin/env python

import socket

host='10.137.24.133'
port=5001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(1)



i=1
m=0
while m<3:
        
    sock, address = s.accept()
    print("connection")

    filepicname= "totally_uni" + str(i) + ".jpg"
    
    f = open(filepicname, "wb") # renamed file
    
    while True:
    
        veri = sock.recv(512)
        if not veri:
            break
        f.write(veri)
    f.close()
    print("picture received.")
    i+=1
    m+=1

sock.close()

s.close()



def recvall(baglanti, buf):

# baglanti  means connection in turkish
    data = ""
    while len(data) < buf:
        packet = baglanti.recv(buf - len(data))
        if not packet:
            return None
        data += packet
    return data

