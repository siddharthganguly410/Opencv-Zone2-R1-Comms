import cv2
import numpy as np
from ultralytics import YOLO
import math
cost_list=[10,20,30,40]# r2,empty,r1,fake
def cost():
    pass
path_list=[]
# def path():
#     for block, value in scroll_dict_empty.items():
#         if value!=scroll_list[0]:
#             path_list.append(block)
    
#     return path_list

scroll_list=["empty","R1 KFS","R2 KFS","Fake"]
scroll_dict_path={"1":{"2":cost_list[1],"4":cost_list[1]},
                  "2":{"1":cost_list[1],"3":cost_list[1],"5":cost_list[1]},
                  "3":{"2":cost_list[1],"6":cost_list[1]},
                  "4":{"5":cost_list[1],"7":cost_list[1]},
                  "5":{"4":cost_list[1],"6":cost_list[1],"8":cost_list[1]},
                  "6":{"5":cost_list[1],"9":cost_list[1]},
                  "7":{"8":cost_list[1],"10":cost_list[1]},
                  "8":{"7":cost_list[1],"9":cost_list[1],"11":cost_list[1]},
                  "9":{"8":cost_list[1],"12":cost_list[1]},
                  "10":{"11":cost_list[1],"end":cost_list[1]},
                  "11":{"10":cost_list[1],"12":cost_list[1],"end":cost_list[1]},
                  "12":{"11":cost_list[1],"end":cost_list[1]}}

scroll_dict_empty={"1":scroll_list[0],
                  "2":scroll_list[0],
                  "3":scroll_list[0],
                  "4":scroll_list[0],
                  "5":scroll_list[0],
                  "6":scroll_list[0],
                  "7":scroll_list[0],
                  "8":scroll_list[0],
                  "9":scroll_list[0],
                  "10":scroll_list[0],
                  "11":scroll_list[0],
                  "12":scroll_list[0]}


model=YOLO("symbol300.pt")
object_width=25
focal=700
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if not ret:
        break
    w,h,c=frame.shape
    results=model.predict(source=frame,conf=0.7,device=0,verbose=False)
    for result in results:
        frame=result.plot()
        for box in result.boxes:
            
            x1,y1,x2,y2=map(int,box.xyxy[0])
            xc=(x1+x2)//2
            
            pixels = x2 - x1
            if pixels != 0:
                
                distance = (focal * object_width) / pixels
                area=(x2-x1)*(y2-y1)
                # focal=(distance*pixels)/object_width
                distance_text = f"{area:.2f}"
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,distance_text , (x1, y1 - 10), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                scroll_dict_empty["3"]=0
                cls_id=int(box.cls[0])
                class_name=model.names[cls_id]

                if 100<=distance<=300:
                    if xc>320:
                        scroll_dict_empty["5"]=class_name
                    else:
                        scroll_dict_empty["6"]=class_name
                elif 300<=distance <=500:
                    if xc>320:
                        scroll_dict_empty["8"]=class_name
                    else:
                        scroll_dict_empty["9"]=class_name
                elif 500<=distance<=800:
                    if xc>320:
                        scroll_dict_empty["11"]=class_name
                    else:
                        scroll_dict_empty["12"]=class_name
                else :
                    pass
        print(scroll_dict_empty)
        
        # path()                          ## PATH AT RUNTIME
        # print(path_list)

            

            
    
                
        cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
# path()
# print(scroll_dict_empty)      ## PATH AT END
# print(path_list)

cap.release()
cv2.destroyAllWindows()