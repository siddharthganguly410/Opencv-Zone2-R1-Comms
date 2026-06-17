# main.py
import cv2
from ultralytics import YOLO
import numpy as np

from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd
from zone2_path import path
FRAME_WIDTH = 640
CAM_FOV = 80
ZONE_1_ACTIVE = True
ZONE_2_ACTIVE = False
process_zone1 = False
model = YOLO("symbol300.pt")
model2 = YOLO("spf6.pt")
cap1 = cv2.VideoCapture(2)   # Zone 2 Left
cap2 = cv2.VideoCapture(0)   
cap3 = cv2.VideoCapture(1)   # Zone 1 Camera
curr_position = [0, 0]
curr_row = 0
curr_column = 0
class_of_next = "Empty"
data_to_next = 0
xr=yr=0
wr=hr=0
xg=yg=0
wg=hg=0
arear=areag=0
scroll_list = ["Empty", "R1 KFS", "R2 KFS", "Fake"]
scroll_dict_empty = {i: "Empty" for i in range(1, 13)}

while True:
    key = cv2.waitKey(1) & 0xFF

    if ZONE_1_ACTIVE:
        ret3, f3 = cap3.read()
        if not ret3:
            break

        hsv3 = cv2.cvtColor(f3, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 60, 180])
        upper_green = np.array([95, 255, 255])

        lower_red1 = np.array([0, 70, 180])
        upper_red1 = np.array([12, 255, 255])
        lower_red2 = np.array([160, 70, 180])
        upper_red2 = np.array([179, 255, 255])

        mask_green = cv2.inRange(hsv3, lower_green, upper_green)
        mask_r = cv2.bitwise_or(cv2.inRange(hsv3, lower_red1, upper_red1),cv2.inRange(hsv3, lower_red2, upper_red2))

        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        results3 = model2.predict(f3, conf=0.9, device=0, verbose=False)

        zone1_xc = None
        for r in results3:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                zone1_xc = (x1 + x2) // 2
                horizontal_offset = zone1_xc - 320
                zone1_angle = (horizontal_offset / FRAME_WIDTH) * CAM_FOV

        if key == ord('z'):
            if zone1_xc is not None and 260 <= zone1_xc <= 380:
                process_zone1 = True
                print("YES | Angle:", zone1_angle)
            else:
                print("NEXT")
                process_zone1 = False
        for cnt in contours_red:
                xr, yr, wr, hr = cv2.boundingRect(cnt)
                arear = wr * hr
        for cnt in contours_green:
                xg, yg, wg, hg = cv2.boundingRect(cnt)
                areag = wg * hg
        if process_zone1:
            
            if 10000 <= arear <= 30000:
                print("ZONE 2")
                ZONE_1_ACTIVE = False
                ZONE_2_ACTIVE = True
                process_zone1 = False
                cv2.destroyWindow('Zone 1')
                
                
            elif 10000 <= areag <= 30000:
                print("REPEAT")
                

        for r in results3:
            f3 = r.plot()
        cv2.line(f3,(260,0),(260,480),(255,0,0),1) # VERTICAL CENTER LINES 1  --ZONE 1
        cv2.line(f3,(380,0),(380,480),(255,0,0),1) # VERTICAL CENTER LINES 2  --ZONE 1
        cv2.imshow("Zone 1", f3)

    if ZONE_2_ACTIVE==True:
        ret1, f1 = cap1.read()
        ret2, f2 = cap2.read()
        if not ret1 or not ret2:
            break
        cv2.line(f1,(0,160),(640,160),(255,0,0),1) 
        cv2.line(f2,(0,160),(640,160),(255,0,0),1)  
        cv2.line(f1,(0,320),(640,320),(255,0,0),1) 
        cv2.line(f2,(0,320),(640,320),(255,0,0),1)
        cv2.line(f1,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
        cv2.line(f2,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
        results1 = model.predict(f1, conf=0.8, device=0, verbose=False)
        results2 = model.predict(f2, conf=0.8, device=0, verbose=False)

        for r in results1:
            f1 = r.plot()
        for r in results2:
            f2 = r.plot()

        cv2.imshow("Left", f1)
        cv2.imshow("Right", f2)

        if key==ord('l'):
            right_class,pos1=rd(results2,f2,model)
            left_class,pos2=ld(results1,f1,model)
            center_class=cd(pos1,pos2)
            for i in scroll_dict_empty:
                if scroll_dict_empty[i]=="Empty" and (i==1 or i==2 or i==3):
                    scroll_dict_empty[1]=right_class
                    scroll_dict_empty[2]=center_class
                    scroll_dict_empty[3]=left_class
            print(curr_position[0])
            curr_position, curr_column, class_of_next,data_to_next=path(scroll_dict_empty,curr_position,curr_column,curr_row,right_class,center_class,left_class,class_of_next)
            print(curr_position[0])
            print(class_of_next)
            print(data_to_next)
        if key==ord('r'):
            right_class,pos1=rd(results2,f2,model)
            left_class,pos2=ld(results1,f1,model)
            center_class=cd(pos1,pos2)
            curr_position, curr_column, class_of_next,data_to_next=path(scroll_dict_empty,curr_position,curr_column,curr_row,right_class,center_class,left_class,class_of_next)
            print("Next_position : ",curr_position[0])
            print("Next_Column",curr_column)
            print("Data :",data_to_next)
            print("Class of next : ",class_of_next)
            print(scroll_dict_empty)

    if key == ord('q'):
        break


if cap1: cap1.release()
if cap2: cap2.release()
if cap3: cap3.release()
cv2.destroyAllWindows()
