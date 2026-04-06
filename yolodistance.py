from ultralytics import YOLO
import cv2
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
            cls_id=int(box.cls[0])
            class_name=model.names[cls_id]
            x1,y1,x2,y2=map(int,box.xyxy[0])
            pixels = x2 - x1
            if pixels != 0:
                
                distance = (focal * object_width) / pixels
                # focal=(distance*pixels)/object_width
                distance_text = f"{distance:.2f}"
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,distance_text , (x1, y1 - 10), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                # print(distance_text)
                

        cv2.imshow('frame',frame)
           
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
# from ultralytics import YOLO
# import cv2

# model = YOLO('spf3.pt')
# print(model.names)
# cap = cv2.VideoCapture(0) 

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model.predict(
#         frame,
#         conf=0.8,
#         device=0,      # GPU
#         verbose=False
#     )

#     for r in results:
#         frame = r.plot()

#     cv2.imshow("Spearhead", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
'''
100-200
300-500
500-700
'''