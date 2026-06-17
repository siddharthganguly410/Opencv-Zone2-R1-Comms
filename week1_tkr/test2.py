import cv2
import numpy as np
import matplotlib.pyplot as plt
image=cv2.imread('phool.jpeg',cv2.IMREAD_COLOR)
cv2.line(image,(0,0),(150,150),(255,255,255),15)
cv2.rectangle(image,(15,25),(200,150),(0,255,0),15)
cv2.circle(image,(100,63),55,(0,0,255),55)
pts=np.array([[10,5],[20,30],[70,20],[500,10]],np.int32)
#pts=pts.reshape((-1,1,2))
cv2.polylines(image,[pts],True,(0,255,255),5)
font=cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image,'OpenCV Tuts',(0,130),font,2,(200,255,255),5,cv2.LINE_AA)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()