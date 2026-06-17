import cv2
import numpy as np
import matplotlib.pyplot as plt
# PART 15
cap=cv2.VideoCapture(0)
fgbg=cv2.createBackgroundSubtractorMOG2()

while True:
    ret,frame=cap.read()
    fgmask=fgbg.apply(frame)
    cv2.imshow('tp',frame)
    cv2.imshow('tp2',fgmask)

    k=cv2.waitKey(0) & 0xff
    if k==27:
        break
    
cap.release()
cv2.destroyAllWindows()