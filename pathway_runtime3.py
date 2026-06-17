import cv2
import numpy as np
from ultralytics import YOLO
cap1=cv2.VideoCapture(0)
cap2=cv2.VideoCapture(1)
model=YOLO("symbol300.pt")
current_position_list=[(0),(0)]
pos1=None
pos2=None
class_name1=class_name2=None
l1=["Empty"]
l2=["Empty"]
l3=["Empty"]
next=["Empty"]

j=1
while True:
    ret1,f1=cap1.read()
    ret2,f2=cap2.read()
    key=cv2.waitKey(1) & 0xFF
    if not ret1:
        break
    if not ret2:
        break
    results1=model.predict(f1,conf=0.8,device=0,verbose=False)
    results2=model.predict(f2,conf=0.8,device=0,verbose=False)
    xlc=xrc=0
    ylc=yrc=0
    cv2.line(f1,(0,160),(640,160),(255,0,0),1) 
    cv2.line(f2,(0,160),(640,160),(255,0,0),1)  
    cv2.line(f1,(0,320),(640,320),(255,0,0),1) 
    cv2.line(f2,(0,320),(640,320),(255,0,0),1) 
    cv2.line(f1,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
    cv2.line(f2,(320,0),(320,480),(255,0,0),1) # VERTICAL CENTER LINES
    
    for result1 in results1:
        f1=result1.plot()
        for box in result1.boxes:
            xl1,yl1,xl2,yl2=map(int,box.xyxy[0])
            xlc=(xl1+xl2)//2
            ylc=(yl1+yl2)//2
            cls_id1=int(box.cls[0])
            class_name1=model.names[cls_id1]
            if class_name1==class_name2 and class_name1==None:
                class_name1=class_name2="Empty"
            
            if 0<=xlc<=320 and 160<=ylc<=320 and key==ord('l') :
                l3[0]=class_name1    
            elif 160<=ylc<=320 and 320<= xlc <= 640 :
                pos1=class_name1
    for result2 in results2:
        f2=result2.plot()
        for box in result2.boxes:
            xr1,yr1,xr2,yr2=map(int,box.xyxy[0])
            xrc=(xr1+xr2)//2
            yrc=(yr1+yr2)//2
            cls_id2=int(box.cls[0])
            class_name2=model.names[cls_id2]
            if 160<=yrc<=320 and 320<=xrc<=640 and key==ord('l') :
                l1[0]=class_name2
            elif 160<= yrc <=320 and 0<= xrc<=320:
                pos2=class_name2
            
    if pos1==pos2 and key==ord('l'):
        l2[0]=pos1         
    
        if l1[0]=="R2Real" and key==ord['l']:
            current_position_list[0]=1
        
        elif l2[0]=="R2Real" and key==ord('l'):
            current_position_list[0]=2
        elif l3[0]=="R2Real" and key==ord('l'):
            current_position_list[0]=3
        
        print(l1,l2,l3)
        print(current_position_list)
    cv2.imshow('Left :',f1)
    cv2.imshow('Right :',f2)
    
    if key==ord('r'):
        current_position_list[1]=j
        j+=1
        print(current_position_list)
    if pos1==pos2 and key==ord('x'):
        if pos1==None:
             next[0]="Empty"
        else:
             next[0]=pos1
        if next[0]=="Fake"  or next[0]=="Rsymbol":
                if current_position_list[0]==1 and current_position_list[0]==3:
                     current_position_list[0]=2
                    
                elif current_position_list[0]==2:
                     current_position_list[0]==1
                     print(current_position_list)
                    
        elif next[0]=="R2Real" or next[0]=="Empty":
                    print("Success")
                    current_position_list[1]=j
                    j+=1
                    if(current_position_list[1]==4):
                        print("exit")
                         
        print(current_position_list)
    
    if key==ord('q'):
        break
    

cap1.release()
cap2.release()
cv2.destroyAllWindows()
