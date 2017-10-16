import cv2
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression
hog=cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cam=cv2.VideoCapture(0)
while True:
    sensor1=1
    sensor2=0
    ret, frame = cam.read()
    frame=imutils.resize(frame, width=min(400, frame.shape[1]))
    orig=frame.copy()
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
    for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    print "rects "+str(len(rects))
    print "picks "+str(len(pick))
    cv2.imshow('test',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if(len(pick)>2):
        print "ouch:"
        exit(0)

    if(sensor2==0 and sensor1==1 and len(pick)<3 ):
        print "allowed"
    else:
        print "denied"
cam.release()
cv2.destroyAllWindows()
