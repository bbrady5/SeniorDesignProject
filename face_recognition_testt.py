# Face recognition with LBP descriptors.
# See Timo Ahonen's "Face Recognition with Local Binary Patterns".
#
# Before running the example:
# 1) Download the AT&T faces database http://www.cl.cam.ac.uk/Research/DTG/attarchive/pub/data/att_faces.zip
# 2) Exract and copy the orl_faces directory to the SD card root.


import sensor, image, pyb, time, uos, machine




#snapshot on face detection
RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

face_cascade = image.HaarCascade("frontalface", stages=25)

# while(True): --- loop whole program //at end

pyb.LED(RED_LED_PIN).on()
print("About to start detecting faces...")
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
print("Now detecting faces!")
pyb.LED(BLUE_LED_PIN).on()

diff = 10 # We'll say we detected a face after 10 frames.
while(diff):
        img = sensor.snapshot()
        faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

        if faces:
            diff -= 1
            for r in faces:
                img.draw_rectangle(r)

pyb.LED(BLUE_LED_PIN).off()
print("Face detected! Saving image...")
pic_name = "snapshot-new2.pgm" # add %d, make a count each time it goes through the loop
sensor.snapshot().save(pic_name) # Save Pic.

#machine.reset()
#uos.chdir("/")
snap_img = image.Image(pic_name).mask_ellipse()

d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))

lbp_list = []
name_list = []

uos.chdir("/Faces")
for filename in uos.listdir("/Faces"):
  if filename.endswith(".jpg") :
    img = None
    img = image.Image(filename).mask_ellipse()
    d1 = img.find_lbp((0, 0, img.width(), img.height()))
    dist = image.match_descriptor(d0, d1)
    lbp_list.append(dist)
    word = filename
    und_loc = word.index('_')
    word = word[0:(und_loc)]

    #print(word)
    name_list.append(word)


    #print("Success")
    continue
  else:
    print("ERROR")

#print(lbp_list)
#print(name_list)

list_set = set(name_list)
# convert the set to the list
unique_list = (list(list_set))
unique_list.reverse()
res = [name_list.index(i) for i in unique_list]


i = 0
x=0


total = 0
i = 0
lbp_unique_list = []
while i < (len(res)-1):
    start = res[i]
    end = res[i+1]
    i+= 1
    j = start
    count = 0
    while j < end :
        total += lbp_list[j]
        j+= 1
        count += 1
    lbp_avg = total/count
    #print(lbp_avg)
    lbp_unique_list.append(lbp_avg)

    total = 0
    count = 0

last = end

while last  < len(lbp_list):
    total += lbp_list[last]
    last+= 1
    count += 1
lbp_avg = total/count
#print(lbp_avg)
lbp_unique_list.append(lbp_avg)
print(lbp_unique_list)
print(min(lbp_unique_list))
name_ind = lbp_unique_list.index(min(lbp_unique_list))
print(name_ind)
print(unique_list[name_ind])
print("The person you are looking at is: " + unique_list[name_ind])
