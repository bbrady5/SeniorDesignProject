import requests
import json
from datetime import datetime
import threading
import os
import shutil
import socket
import time

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
