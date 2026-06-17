import cv2
import os

folder = "captured_frames"
os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Webcam", frame)

    # Press 's' to save a frame
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        img_name = f"{folder}/frame_{frame_count}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"Saved: {img_name}")
        frame_count += 1
    
    # Press 'q' to Quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
