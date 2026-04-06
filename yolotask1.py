from ultralytics import YOLO
import cv2

model = YOLO('spf3.pt')

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame,conf=0.8,device=0,verbose=True)

    for r in results:
        frame = r.plot()

    cv2.imshow("Spearhead", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# import cv2
# from ultralytics import YOLO
# a = cv2.VideoCapture(0)
# b = cv2.VideoCapture(1)
# model = YOLO("spf3.pt")
# focal=700
# base_line=15

# while True:
#     _,f1=a.read()
#     _,f2=b.read()
#     # f1=cv2.flip(f1,1)
#     h1,w1,c1 = f1.shape
#     cv2.circle(f1,(w1//2,h1//2),5,(0,0,0),-1,lineType=cv2.LINE_AA)
#     h2,w2,c2 = f2.shape
#     cv2.circle(f2,(w1//2,h2//2),5,(0,0,0),-1,lineType=cv2.LINE_AA)
#     results1 = model(f1,device=0,conf=0.7)
#     results2 = model(f2,device=0,conf=0.7)

#     xl = yl = None
#     xr = yr = None
#     for r in results1:
#         for box in r.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             xl=(x1+x2)//2
#             yl=(y1+y2)//2
#             cv2.circle(f1,(xl,yl),5,(0,0,0),-1,lineType=cv2.LINE_AA)
#             cv2.rectangle(f1,(x1,y1),(x2,y2),(0,0,0),3,lineType=cv2.LINE_AA)
#     for r in results2:
#         for box in r.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             xr=(x1+x2)//2
#             yr=(y1+y2)//2
#             cv2.circle(f2,(xr,yr),5,(0,0,0),-1,lineType=cv2.LINE_AA)
#             cv2.rectangle(f2,(x1,y1),(x2,y2),(0,0,0),3,lineType=cv2.LINE_AA)

#     if xl != None and xr != None:
#         disparity = xl-xr
#         cv2.putText(f1,f"Disparity: {disparity:.2f} px ",(10,h1//2),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
#         cv2.putText(f2,f"Disparity: {disparity:.2f} px",(10,h2//2),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
#         if disparity!=0:
#             distance=focal*base_line/disparity
#             Dist = str(distance)
#             side_ways_dist = (distance*xl)/focal
#             Side_DIST = str(side_ways_dist)
#             cv2.putText(f1,f"Distance Z: {distance:.2f}",((w1//2)-200,(h1//2)+200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
#             cv2.putText(f2,f"Distance Z: {distance:.2f}",((w2//2)-200,(h2//2)+200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
#             cv2.putText(f1,f"Distance X: {side_ways_dist:.2f}",((w2//2)-200,(h2//2)-200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)
#             cv2.putText(f2,f"Distance X: {side_ways_dist:.2f}",((w2//2)-200,(h2//2)-200),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA,False)



#     cv2.imshow("Left Camera",f1)
#     cv2.imshow("Right Camera",f2)
   
#     if cv2.waitKey(1) & 0xFF==ord('q'):
#         break

# a.release()
# b.release()
# cv2.destroyAllWindows()