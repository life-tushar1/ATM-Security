import mraa
import time
import os
import sys
import cv2
import numpy as np
import imutils
allowed=mraa.Gpio(48)
allowed.dir(mraa.DIR_OUT)
door=mraa.Gpio(36)
door.dir(mraa.DIR_IN)
fd=0
fv=0
fc=0
vib=mraa.Gpio(47)
door.dir(mraa.DIR_IN)
ag=0
ad=0
fac=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FPS, 30)
while True:
    ret, frame = cam.read()
    frame=imutils.resize(frame, width=min(500, frame.shape[1]))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face=fac.detectMultiScale(gray,1.3,5)
    if(door.read()==1):
	       fd=0
    else:
	       if(fd==0):
		             print "Entry door is open.. your access is denied "
                     time.sleep(3)
  	       fd+=1
    if(len(face)<3):
	       fc=0
    else:
	       if(fc==0):
                print "too many people around..your access is denied "
                time.sleep(3)
           fc+=1
    if(vib.read()==0):
	       fv=0

    else:
	       if(fv==0):
                print "dont fiddle with the machine....your access is denied"
                time.sleep(5)
            fv+=1
    if(fv==fc==fd==0):
	       if(ag==0):
		             os.system('clear')
                    print "access granted"
	       ag+=1
	       ad=0
    else:
	       if(ad==0):
		             os.system('clear')
                     print "access denined"
	      ad+=1
          ag=0
    if(len(face)>0):
          allowed.write(1)
    else:
          allowed.write(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
cam.release()
cv2.destroyAllWindows()
