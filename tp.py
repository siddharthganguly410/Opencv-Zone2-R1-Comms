import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def red():
    print("red")

def green():
    print("green")

def blue():
    print("blue")

def purple():
    print("purple")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ----- RED (two ranges in HSV) -----
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    # ----- GREEN -----
    lower_green = np.array([50, 120, 50])
    upper_green = np.array([95, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # ----- BLUE -----
    lower_blue = np.array([90, 50, 70]) 
    upper_blue = np.array([128, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_purple = np.array([150, 0, 150]) 
    upper_purple = np.array([255, 80, 255])
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    cv2.line(frame,(0,240),(640,240),(255,0,0),1)
    # Detection
    if cv2.countNonZero(mask_red) > 5000:
        red()
    elif cv2.countNonZero(mask_blue) > 5000:
        blue()
    elif cv2.countNonZero(mask_green) > 5000:
        green()
    elif cv2.countNonZero(mask_purple) > 5000:
        purple()
    else:
        pass

    cv2.imshow("Frame", frame)

    # Correct way to exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()