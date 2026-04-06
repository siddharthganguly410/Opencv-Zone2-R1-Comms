from ultralytics import YOLO
import cv2
model=YOLO('spf3.pt')
cap=cv2.VideoCapture(0)
cap2=cv2.VideoCapture(1)
baseline=9
focal=750
#depth=50
while True:
    ret,frame=cap.read()
    w1,h1,c1=frame.shape
    
    ret2,frame2=cap2.read()
    
    xl=yl=None
    xr=yr=None
    if not ret:
        break
    results=model.predict(frame,conf=0.8,device=0,verbose=False)
    results2=model.predict(frame2,conf=0.8,device=0,verbose=False)
    for result in results:
        frame=result.plot()

        for box in result.boxes.xyxy:
            x1,y1,x2,y2=map(int,box)
            xl=(x1+x2)//2
            yl=(y1+y2)//2
    
    for result2 in results2:
        frame2=result2.plot()

        for box in result2.boxes.xyxy:
            x1,y1,y1,y2=map(int,box)
            xr=(x1+x2)//2
            yr=(y1+y2)//2

    if xl!=None and xr!=None:
        disparity=xl-xr
        if disparity!=0:
            depth=focal*baseline/disparity
            #focal=(depth*disparity)/baseline
            Dist=str(depth)
            cv2.putText(frame,f"Distance : {Dist}",(200,200),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1,cv2.LINE_AA,False)
            cv2.putText(frame2,f"Distance : {Dist}",(200,200),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),1,cv2.LINE_AA,False)

    cv2.imshow('frame 1',frame)
    cv2.imshow('frame 2',frame2)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break


cap.release()
cap2.release()
cv2.destroyAllWindows
