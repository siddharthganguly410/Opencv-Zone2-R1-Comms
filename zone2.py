# main.py
import cv2
from ultralytics import YOLO

from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd
from zone2_path import path 
import numpy as np

process_zone1 = False
zone1_angle = None
zone1_xc = None
zone1_yc = None
msg=None
FRAME_WIDTH = 640
CAM_FOV = 80
areag=arear=0
xr=yr=0
xg=yg=0
wr=hr=0
wg=hg=0

model = YOLO("symbol240_9.pt")
model2=YOLO("spf3.pt")

cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)
cap3 = cv2.VideoCapture(1)
curr_position=[0,0]
curr_row=0
curr_column=0
data_to_next=0
left_class = "Empty"
right_class = "Empty"
center_class = "Empty"
pos1 = "Empty"
pos2 = "Empty"
class_of_next="Empty"
scroll_list = ["Empty", "R1 KFS", "R2 KFS", "Fake"]
scroll_dict_empty={1:scroll_list[0],
                   2:scroll_list[0],
                   3:scroll_list[0],
                   4:scroll_list[0],
                   5:scroll_list[0],
                   6:scroll_list[0],
                   7:scroll_list[0],
                   8:scroll_list[0],
                   9:scroll_list[0],
                   10:scroll_list[0],
                   11:scroll_list[0],
                   12:scroll_list[0]}


while True:
    ret1, f1 = cap1.read()
    ret2, f2 = cap2.read()
    ret3,f3=cap3.read()
    if not ret1 or not ret2 : #or not ret3
        break

    key = cv2.waitKey(1) & 0xFF
    hsv3 = cv2.cvtColor(f3, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 60, 180])
    upper_green = np.array([95, 255, 255])

    lower_red1 = np.array([0, 70, 180])
    upper_red1 = np.array([12, 255, 255])

    lower_red2 = np.array([160, 70, 180])
    upper_red2 = np.array([179, 255, 255])


    mask_green = cv2.inRange(hsv3, lower_green, upper_green)
    mask_r1 = cv2.inRange(hsv3, lower_red1, upper_red1)
    mask_r2 = cv2.inRange(hsv3, lower_red2, upper_red2)
    mask_r = cv2.bitwise_or(mask_r1, mask_r2)
    contours_green, hierarchy1 = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, hierarchy2 = cv2.findContours(mask_r, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    results1 = model.predict(f1, conf=0.8, device=0, verbose=False)
    results2 = model.predict(f2, conf=0.8, device=0, verbose=False)
    results3 = model2.predict(f3,conf=0.9,device=0,verbose=False)
    cv2.line(f1,(0,160),(640,160),(255,0,0),1) 
    cv2.line(f2,(0,160),(640,160),(255,0,0),1)  
    cv2.line(f1,(0,320),(640,320),(255,0,0),1) 
    cv2.line(f2,(0,320),(640,320),(255,0,0),1)
    cv2.line(f1,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
    cv2.line(f2,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
    cv2.line(f3,(260,0),(260,480),(255,0,0),1) # VERTICAL CENTER LINES 1  --ZONE 1
    cv2.line(f3,(380,0),(380,480),(255,0,0),1) # VERTICAL CENTER LINES 2  --ZONE 1
    cv2.circle(f3,(320,240), 3, (0, 255, 0), -1)
    for result1 in results1:
        f1=result1.plot()
    for result2 in results2:
        f2=result2.plot()
    
    
    
    
    
    cv2.imshow("Left", f1)
    cv2.imshow("Right", f2)
    # cv2.imshow("Zone 1 :",f3)
    
    
    zone1_xc = zone1_yc = zone1_angle = None

    for r in results3:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            zone1_xc = (x1 + x2) // 2
            zone1_yc = (y1 + y2) // 2

            horizontal_offset = zone1_xc - 320
            zone1_angle = (horizontal_offset / FRAME_WIDTH) * CAM_FOV

    

    if key == ord('z'):
        if zone1_xc is not None and 260 <= zone1_xc <= 380:
            print("YES")
            print("Angle:", zone1_angle)
            process_zone1=True
        else:
            print("Next")
            process_zone1=False

    if len(contours_green) > 0:
        for cnt in contours_green:
            xg, yg, wg, hg = cv2.boundingRect(cnt)
            # cv2.rectangle(f3, (xg, yg), (xg+wg, yg+hg), (0, 255, 0), 2)
            areag=wg*hg
            # cv2.putText(f3, f"{areag:.2f}",(xg + 20, yg - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)
            if 9000<=areag<=30000 and process_zone1:
                cv2.rectangle(f3, (xg, yg), (xg+wg, yg+hg), (0, 255, 0), 2)
                print("REPEAT")
    if len(contours_red) > 0:
        for cnt in contours_red:
            xr, yr, wr, hr = cv2.boundingRect(cnt)
            # cv2.rectangle(f3, (xr, yr), (xr+wr, yr+hr), (0, 255, 0), 2)
            arear=wr*hr
            # cv2.putText(f3, f"{arear:.2f}",(xr + 20, yr - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)
            if 9000<=arear<=30000 and process_zone1:
                cv2.rectangle(f3, (xr, yr), (xr+wr, yr+hr), (0, 255, 0), 2)
                print("ZONE 2")        
    # if arear!=0 or areag!=0 and process_zone1==True:
    #     if 25000<=arear<=40000:
    #         cv2.rectangle(f3, (xr, yr), (xr+wr, yr+hr), (0, 255, 0), 2)
    #         print("ZONE 2")
    #     elif 25000<= areag<=40000 and process_zone1==True :
    #         cv2.rectangle(f3, (xg, yg), (xg+wg, yg+hg), (0, 255, 0), 2)
    #         print("REPEAT")
    #     else:
    #         pass

    
    # if key==ord('m'):
    #     if process_zone1==True:
    #         if cv2.countNonZero(mask_green) > 0:
    #             msg="REPEAT"
    #             print(msg)
    #         elif cv2.countNonZero(mask_r) > 0:
    #             msg="ZONE2"
    #             print(msg)

    # if len(contours_green) > 0:
    #     for cnt in contours_green:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(f3, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #         area=w*h
    #         cv2.putText(f3, f"{area:.2f}",(x + 20, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)
    # if len(contours_red) > 0:
    #     for cnt in contours_red:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(f3, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #         area=w*h
    #         cv2.putText(f3, f"{area:.2f}",(x + 20, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)


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
    
    for result3 in results3:
        f3=result3.plot()
    
    cv2.imshow('Zone 1',f3)
    
    
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

cap1.release()
cap2.release()
cv2.destroyAllWindows()
