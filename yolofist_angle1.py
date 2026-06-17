from ultralytics import YOLO
import cv2
import math

model = YOLO('yolov8s.pt')

object_width = 8.2
focal = 740  

FRAME_CENTER = (240,320)

FRAME_CENTER1= (320,240)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.25, verbose=False)

    for result in results:
        annotated_frame = result.plot()

        
        cv2.putText(annotated_frame, "center", (330,250),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.circle(annotated_frame, FRAME_CENTER1, 3, (0,255,0), -1)

        cx0, cy0 = FRAME_CENTER1

        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            x = (x1 + x2) // 2  
            y = (y1 + y2) // 2

            # Horizontal pixels
            horizontal = x - cx0

            
            angle_rad = math.atan(horizontal / focal)

            
            angle_deg = math.degrees(angle_rad)

            # Draw center point
            cv2.circle(annotated_frame, (x, y), 3, (0, 255, 0), -1)

            # Display angle
            cv2.putText(annotated_frame, f"{angle_deg:.2f}",(x1 + 150, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0), 2)

        cv2.imshow("YOLO Webcam", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
