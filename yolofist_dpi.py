from ultralytics import YOLO
import cv2
import math

model = YOLO('fist_v5.pt')
dpi=137
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    results = model.predict(source=frame, conf=0.25, verbose=False)
    
    for result in results:
        
        annotated_frame = result.plot()
        cv2.putText(annotated_frame,f"240,320",(250,330),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
        cv2.circle(annotated_frame,(240,320),2,(0,255,0))

        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            x = (x1 + x2) // 2
            y = (y1 + y2) // 2

            
            dist_2 = math.sqrt((240 - x)**2)#+ (320 - y)**2
            pixels = x2 - x1

            if pixels != 0:
                dist_1 = math.sqrt(x**2 + y**2)

               
                if dist_1 != 0 :
                    angle = math.asin(dist_2 / dist_1)
                    angle_deg = math.degrees(angle)
                    
                    cv2.putText(annotated_frame,f"{x,y}",(x+5,y+5),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
                    cv2.circle(annotated_frame,(x,y),2,(0,255,0))
                    if x<240:
                        angle_deg=-angle_deg
                        cv2.putText(annotated_frame,f"{angle_deg:.2f}",(x1+150, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
                    else:
                        angle_deg=angle_deg
                        cv2.putText(annotated_frame,f"{angle_deg:.2f}",(x1+150, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)

        cv2.imshow("YOLOv5 Webcam", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
