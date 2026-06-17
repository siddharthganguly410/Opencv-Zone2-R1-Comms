import cv2
import numpy as np

# taking the input from webcam
vid = cv2.VideoCapture(0)

# def mouse_click(event, x, y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         b,g,r = img[y,x]  
#         text = f"({x},{y}) BGR=({b},{g},{r})"

#         font = cv2.FONT_HERSHEY_TRIPLEX
#         cv2.putText(img, text, (x, y), font, 0.5, (255, 255, 0), 1)
#         cv2.imshow('frame', img)
#         print((x,y),text)
        
def mouse_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        b, g, r = img[y, x]

        # Convert single pixel BGR to HSV
        pixel = np.uint8([[[b, g, r]]])
        hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)

        h, s, v = hsv[0][0]

        text = f"({x},{y}) BGR=({b},{g},{r}) HSV=({h},{s},{v})"

        cv2.putText(
            img,
            text,
            (x, y),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            (255,255,0),
            1
        )

        cv2.imshow('frame', img)

        print(text)
    elif event == cv2.EVENT_RBUTTONDOWN:
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        text = 'Right Button'
        cv2.putText(img, text, (x, y), font, 0.7, (0, 255, 255), 2)
        cv2.imshow('frame', img)

while True:
    _, img= vid.read()
    cv2.imshow("frame", img)
    cv2.setMouseCallback('frame', mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()

