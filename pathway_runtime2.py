import cv2
import numpy as np
from ultralytics import YOLO

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
model = YOLO("symbol300.pt")

current_position_list = [0, 0]
pos1 = None
pos2 = None

l1, l2, l3 = [], [], []

i = 0
j=1
def handle_key_append(xc, yc, class_name, cam, key, l1, l2, l3, pos1, pos2):
  
    if key != ord('l'):
        return pos1, pos2

    if cam == 'left':
        if 0 <= xc <= 320 and 160 <= yc <= 320:
            l3.append(class_name)
        elif 320 <= xc <= 640 and 160 <= yc <= 320:
            pos1 = class_name

    elif cam == 'right':
        if 320 <= xc <= 640 and 160 <= yc <= 320:
            l1.append(class_name)
        elif 0 <= xc <= 320 and 160 <= yc <= 320:
            pos2 = class_name
    if pos1 == pos2 and pos1 is not None:
        l2.append(pos1)
    
    if i < len(l1) and l1[i] == "R2Real":
        current_position_list[0] = 1
    elif i < len(l2) and l2[i] == "R2Real":
        current_position_list[0] = 2
    elif i < len(l3) and l3[i] == "R2Real":
        current_position_list[0] = 3
    return pos1, pos2

def handle_position_update(key, current_position_list, j):
    if key == ord('r'):
        current_position_list[1] = j
        j += 1
    return ord('l'), j


while True:
    ret1, f1 = cap1.read()
    ret2, f2 = cap2.read()
    key = cv2.waitKey(1) & 0xFF

    if not ret1 or not ret2:
        break

    results1 = model.predict(f1, conf=0.8, device=0, verbose=False)
    results2 = model.predict(f2, conf=0.8, device=0, verbose=False)

    # Draw grid
    cv2.line(f1,(0,160),(640,160),(255,0,0),1) 
    cv2.line(f2,(0,160),(640,160),(255,0,0),1)  
    cv2.line(f1,(0,320),(640,320),(255,0,0),1) 
    cv2.line(f2,(0,320),(640,320),(255,0,0),1) 
    cv2.line(f1,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
    cv2.line(f2,(320,0),(320,480),(255,0,0),1)
    # LEFT CAMERA
    for result in results1:
        f1 = result.plot()
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc = (x1 + x2) // 2
            yc = (y1 + y2) // 2
            class_name = model.names[int(box.cls[0])]

            pos1, pos2 = handle_key_append(
                xc, yc, class_name, "left", key,
                l1, l2, l3, pos1, pos2
            )

    # RIGHT CAMERA
    for result in results2:
        f2 = result.plot()
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc = (x1 + x2) // 2
            yc = (y1 + y2) // 2
            class_name = model.names[int(box.cls[0])]

            pos1, pos2 = handle_key_append(
                xc, yc, class_name, "right", key,
                l1, l2, l3, pos1, pos2
            )

    key,j= handle_position_update(key, current_position_list,j)


    cv2.imshow("Left", f1)
    cv2.imshow("Right", f2)

    print(l1, l2, l3)
    print(current_position_list)

    if key == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
