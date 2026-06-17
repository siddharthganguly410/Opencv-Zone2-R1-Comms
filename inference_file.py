from ultralytics import YOLO
import cv2
import time

model = YOLO("agri_m_v26.pt")

a = cv2.VideoCapture(0)
curr_t = 0
prev_t = 0
fps = 0

while True:
    _,frame = a.read()

    curr_t = time.time()
    fps = 1/(curr_t - prev_t)
    prev_t = curr_t
    h,w,c = frame.shape
    cv2.putText(frame, f"fps: {fps:.1f}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 0, 255), 2)

    results = model(frame,conf=0.8,device=0)
    for r in results:
        
        for box in r.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

    
    cv2.imshow("f",frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

a.release()
cv2.destroyAllWindows()
