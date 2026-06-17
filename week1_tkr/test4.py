import cv2
import numpy as np
import matplotlib.pyplot as plt

# PART 5
i1 = cv2.imread('phool.jpeg')
i_90 = cv2.rotate(i1, cv2.ROTATE_90_CLOCKWISE)
i_180 = cv2.rotate(i1, cv2.ROTATE_180)
i_270 = cv2.rotate(i1, cv2.ROTATE_90_COUNTERCLOCKWISE)

while True:
    cv2.imshow('image', i1)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    if cv2.waitKey(0) & 0xFF == ord('0'):
        
       cv2.destroyAllWindows() 
       cv2.imshow('image', cv2.rotate(i1,cv2.ROTATE_90_CLOCKWISE))
    
    if cv2.waitKey(0) & 0xFF == ord('0'):
       cv2.destroyAllWindows()
       cv2.imshow('image', cv2.rotate(i1,cv2.ROTATE_180))
       
    if cv2.waitKey(0) & 0xFF == ord('0'):
       cv2.destroyAllWindows()
       cv2.imshow('image', cv2.rotate(i1,cv2.ROTATE_90_COUNTERCLOCKWISE))
    
    if cv2.waitKey(0) & 0xFF == ord('0'):
       cv2.destroyAllWindows()
       cv2.imshow('image', i1)
    cv2.destroyAllWindows()   
    
    

       

cv2.destroyAllWindows()
