import cv2
from ultralytics import YOLO
import numpy as np
from itertools import groupby

cmd='0'

cap = cv2.VideoCapture(0)
model = YOLO("symbol300.pt")

cmd_dict = {
    "1": [],  # R2
    "2": [],  # R1
    "3": []   # Empty
}
cmd_list = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.7, device=0, verbose=False)

    current_classes = []

    for result in results:
        frame = result.plot()
        for box in result.boxes:
            x1,y1,x2,y2=map(int,result.boxes.xyxy[0])
            yc=(y1+y2)//2
            if 120<=yc<=360:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                current_classes.append(cls_name)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    
    
    if key == ord('0'):
        break
    elif key==ord('1'):
        cmd=chr(key)
        for cls in current_classes:
            cmd_dict[cmd].append(cls)
            cmd_list.append(cls)
        print(f"Command {cmd} pressed")
        print("Command dict:", cmd_dict)
        print("Common list:", cmd_list)
    elif key==ord('2'):
        cmd=chr(key)
        for cls in current_classes:
            cmd_dict[cmd].append(cls)
            cmd_list.append(cls)
        print(f"Command {cmd} pressed")
        print("Command dict:", cmd_dict)
        print("Common list:", cmd_list)
    elif key==ord('3'):
        cmd=chr(key)
        for cls in current_classes:
            cmd_dict[cmd].append(cls)
            cmd_list.append(cls)
        print(f"Command {cmd} pressed")
        print("Command dict:", cmd_dict)
        print("Common list:", cmd_list)
    

    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
