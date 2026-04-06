from ultralytics import YOLO
import cv2

# Load your trained model or a pretrained YOLOv5 model
model = YOLO('spf4.pt')  # replace with your weights
object_width=8.2
focal=740

# Camera settings
cap = cv2.VideoCapture(0)  # 0 for default webcam          # Real width of object in same units as distance

while True:
    ret, frame = cap.read()
    if not ret:
        break
    w,h,c = frame.shape
    cv2.circle(frame,(h//2,w//2),5,(0,0,0))
    # Run inference on the frame
    results = model.predict(source=frame, conf=0.25, verbose=False)
    
    # Get detections for this frame
    for result in results:  # list of Result objects
        annotated_frame = result.orig_img.copy()  # annotated image with boxes
        
        for box in result.boxes.xyxy:  # xyxy coordinates of each box
            x1, y1, x2, y2 = map(int, box)

            # Calculate object width in pixels
            pixels = x2 - x1
            if pixels != 0:
                
                distance = (focal * object_width) / pixels
                # focal=(distance*pixels)/object_width
                distance_text = f"{distance:.2f}"
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(annotated_frame,distance_text , (x1, y1 - 10), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                print(distance_text)
                

        # Display the annotated frame
        cv2.imshow("YOLOv5 Webcam", annotated_frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
