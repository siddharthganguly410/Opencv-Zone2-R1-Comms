import cv2
import numpy as np
import matplotlib.pyplot as plt

#PART 4

image=cv2.imread('phool.jpeg',cv2.IMREAD_COLOR)
px=image[55,55]
print(px)

roi=image[100:150,100:150]
print(roi)

image[100:150,100:150]=[255,255,255]
phool_face=image[37:111,107:194]
image[0:74,0:87]=phool_face


cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows() 



# # PART 5
# i1=cv2.imread('3D-Matplotlib.png')
# i2=cv2.imread('mainlogo.png')
# r,c,ch=i2.shape
# roi=i1[0:r,0:c]
# i2g=cv2.cvtColor(i2,cv2.COLOR_BGR2GRAY)
# ret,mask=cv2.threshold(i2g,220,255,cv2.THRESH_BINARY_INV)
# mask_inv=cv2.bitwise_not(mask)
# i1_bg=cv2.bitwise_and(roi,roi,mask=mask_inv)
# i2_fg=cv2.bitwise_and(i2,i2,mask=mask)
# dst=cv2.add(i1_bg,i2_fg)
# i1[0:r,0:c]=dst

'''

add=i1+i2
wtd=cv2.addWeighted(i1,0.6,i2,0.4,0)


cv2.imshow('res',i1)
cv2.imshow('mask_inv',mask_inv)
cv2.imshow('image1_bg',i1_bg)
cv2.imshow('image2_fg',i2_fg)

cv2.waitKey(0)
cv2.destroyAllWindows()

'''