import cv2
import numpy as np

#PART 6
'''
img=cv2.imread('bookpage.jpg')
retval,threshold=cv2.threshold(img,12,255,cv2.THRESH_BINARY)
grayscaled=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
retval2,threshold2=cv2.threshold(grayscaled,12,255,cv2.THRESH_BINARY)
gaus=cv2.adaptiveThreshold(grayscaled,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
retval2,otsu=cv2.threshold(grayscaled,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('og',img)
cv2.imshow('thres',threshold)
cv2.imshow('thres2',threshold2)
cv2.imshow('gaus',gaus)
cv2.imshow('otsu',otsu)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
#PART 7-9
cap=cv2.VideoCapture(0)
while True:
    _,frame=cap.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_red=np.array([100,100,50])
    upper_red=np.array([180,255,150])
    
    mask=cv2.inRange(hsv,lower_red,upper_red)
    res=cv2.bitwise_and(frame,frame,mask=mask)
    kernel=np.ones((5,5),np.uint8)
    erosion=cv2.erode(mask,kernel,iterations=1)
    dilation=cv2.dilate(mask,kernel,iterations=1)
    opening=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    closing=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

    #kernel=np.ones((15,15),np.float32)/225
    #smoothed=cv2.filter2D(res,-1,kernel)

    #blur=cv2.GaussianBlur(res,(15,15),0)
    #median=cv2.medianBlur(res,15)
    #bilateral=cv2.bilateralFilter(res,15,75,75)

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('erosion',erosion)
    #cv2.imshow('dilation',dilation)
    #cv2.imshow('opening',opening)
    #cv2.imshow('closing',closing)
    #cv2.imshow('smoothed',smoothed)
    #cv2.imshow('blur',blur)
    #cv2.imshow('median',median)
    #cv2.imshow('bilateral',bilateral)
    
    k=cv2.waitKey(5) & 0xFF
    if k==27:
        break

cv2.destroyAllWindows()
cap.release()