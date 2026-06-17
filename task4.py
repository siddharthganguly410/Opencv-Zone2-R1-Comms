import numpy as np
import cv2

cap = cv2.VideoCapture(0)
clickcolor = np.array([0, 0, 0], dtype=np.uint8)

def mouse_click(event, x, y, flags, param):
    global clickcolor
    if event == cv2.EVENT_LBUTTONDOWN:
         clickcolor = frame[y, x]
         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
         
         clickcolor_hsv = cv2.cvtColor(np.uint8([[clickcolor]]), cv2.COLOR_BGR2HSV)[0][0]
 
         lower = np.array([max(0, clickcolor_hsv[0] - 20), 50, 50])
         upper = np.array([min(179, clickcolor_hsv[0] + 20), 255, 255])
         

         mask = cv2.inRange(hsv, lower, upper)
         res= cv2.bitwise_and(frame, frame, mask=mask)
         cv2.imshow('frame',mask)      
      #  
      #   while True:
      #         cv2.imshow('frame', res)
      #         if cv2.waitKey(1) & 0xFF ==1:
      #              break

#'3'

while True:
  ret, frame = cap.read()
  cv2.imshow('frame', frame)
  if not ret:
        break  
  cv2.setMouseCallback('frame', mouse_click)  
  if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
