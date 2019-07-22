# Untitled - By: BB070512 - Sat Jul 20 2019

import sensor, image, pyb, time
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
pic_name = "snapshot-new.pgm" # add %d, make a count each time it goes through the loop
sensor.snapshot().save(pic_name) # Save Pic.

# face recognition
NUM_SUBJECTS = 5
NUM_SUBJECTS_IMGS = 10

img = image.Image(pic_name).mask_ellipse()
d0 = img.find_lbp((0, 0, img.width(), img.height()))
img = None

print("")
for s in range(1, NUM_SUBJECTS+1):
    dist = 0
    for i in range(2, NUM_SUBJECTS_IMGS+1):
        img = image.Image("orl_faces/s%d/%d.pgm"%(s, i)).mask_ellipse()
        d1 = img.find_lbp((0, 0, img.width(), img.height()))
        dist += image.match_descriptor(d0, d1)
    print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
