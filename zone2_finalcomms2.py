import cv2
from ultralytics import YOLO
import numpy as np
import serial
import time
from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd
from zone2_path import path

FRAME_WIDTH = 640
CAM_FOV = 80

# ------------------ SERIAL INIT ------------------
try:
    ser = serial.Serial('COM5', 9600, timeout=0.01)
    time.sleep(2)
except:
    print("Serial not connected")
    ser = None

# ------------------ FLAGS ------------------
ZONE_1_ACTIVE = True
ZONE_2_ACTIVE = False
process_zone1 = False

# ------------------ LOAD MODELS ------------------
model = YOLO("symbol240_9.pt")
model2 = YOLO("spf4.pt")

# ------------------ CAMERA INIT ------------------
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap3 = cv2.VideoCapture(2)

# Validate cameras
if not cap1.isOpened():
    print("Camera 0 failed")
if not cap2.isOpened():
    print("Camera 1 failed")
if not cap3.isOpened():
    print("Camera 2 failed")

# Reduce resolution (important for performance)
for cap in [cap1, cap2, cap3]:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ------------------ VARIABLES ------------------
curr_position = [0, 0]
curr_row = 0
curr_column = 0
class_of_next = "Empty"
data_to_next = 0

scroll_dict_empty = {i: "Empty" for i in range(1, 13)}

# ------------------ MAIN LOOP ------------------
while True:
    key = None

    # -------- SERIAL READ --------
    if ser and ser.in_waiting:
        try:
            key = ser.readline().decode(errors='ignore').strip().lower()
            if key:
                key = key[0]
            print("Received:", key)
        except:
            key = None

    # ================= ZONE 1 =================
    if ZONE_1_ACTIVE:
        ret3, f3 = cap3.read()
        if not ret3:
            print("Zone 1 camera failed")
            continue

        # Resize for performance
        f3 = cv2.resize(f3, (640, 480))

        hsv3 = cv2.cvtColor(f3, cv2.COLOR_BGR2HSV)

        # Masks
        lower_green = np.array([35, 60, 180])
        upper_green = np.array([95, 255, 255])

        lower_red1 = np.array([0, 70, 180])
        upper_red1 = np.array([12, 255, 255])
        lower_red2 = np.array([160, 70, 180])
        upper_red2 = np.array([179, 255, 255])

        mask_green = cv2.inRange(hsv3, lower_green, upper_green)
        mask_red = cv2.bitwise_or(
            cv2.inRange(hsv3, lower_red1, upper_red1),
            cv2.inRange(hsv3, lower_red2, upper_red2)
        )

        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # -------- YOLO (lighter) --------
        results3 = model2.predict(f3, conf=0.5, device=0, verbose=False)

        zone1_xc = None
        for r in results3:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                zone1_xc = (x1 + x2) // 2

        if zone1_xc is not None:
            offset = zone1_xc - 320
            zone1_angle = (offset / FRAME_WIDTH) * CAM_FOV

        # -------- KEY LOGIC --------
        if key == 'z':
            if zone1_xc is not None and 260 <= zone1_xc <= 380:
                process_zone1 = True
                print("YES | Angle:", zone1_angle)
            else:
                print("NEXT")
                process_zone1 = False

        # -------- LARGEST CONTOUR --------
        arear = 0
        for cnt in contours_red:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area > arear:
                arear = area

        areag = 0
        for cnt in contours_green:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if area > areag:
                areag = area

        # -------- ZONE SWITCH --------
        if process_zone1:
            if 10000 <= arear <= 30000:
                print("ZONE 2")
                ZONE_1_ACTIVE = False
                ZONE_2_ACTIVE = True
                process_zone1 = False

            elif 10000 <= areag <= 30000:
                print("REPEAT")

        # Draw YOLO boxes
        for r in results3:
            f3 = r.plot()

        # Draw guides
        cv2.line(f3, (260, 0), (260, 480), (255, 0, 0), 1)
        cv2.line(f3, (380, 0), (380, 480), (255, 0, 0), 1)

        cv2.imshow("Zone 1", f3)

    # ================= ZONE 2 =================
    if ZONE_2_ACTIVE:
        ret1, f1 = cap1.read()
        ret2, f2 = cap2.read()

        if not ret1 or not ret2:
            print("Zone 2 camera failed")
            continue

        f1 = cv2.resize(f1, (640, 480))
        f2 = cv2.resize(f2, (640, 480))

        # Guides
        for f in [f1, f2]:
            cv2.line(f, (0, 160), (640, 160), (255, 0, 0), 1)
            cv2.line(f, (0, 320), (640, 320), (255, 0, 0), 1)
            cv2.line(f, (320, 0), (320, 480), (255, 0, 0), 1)

        # YOLO
        results1 = model.predict(f1, conf=0.6, device=0, verbose=False)
        results2 = model.predict(f2, conf=0.6, device=0, verbose=False)

        for r in results1:
            f1 = r.plot()
        for r in results2:
            f2 = r.plot()

        cv2.imshow("Left", f1)
        cv2.imshow("Right", f2)

        # -------- ACTION KEYS --------
        if key == 'l':
            right_class, pos1 = rd(results2, f2, model)
            left_class, pos2 = ld(results1, f1, model)
            center_class = cd(pos1, pos2)

            scroll_dict_empty[1] = right_class
            scroll_dict_empty[2] = center_class
            scroll_dict_empty[3] = left_class

            curr_position, curr_column, class_of_next, data_to_next = path(
                scroll_dict_empty, curr_position, curr_column, curr_row,
                right_class, center_class, left_class, class_of_next
            )

            print("Position:", curr_position)
            print("Next class:", class_of_next)

        if key == 'r':
            right_class, pos1 = rd(results2, f2, model)
            left_class, pos2 = ld(results1, f1, model)
            center_class = cd(pos1, pos2)

            curr_position, curr_column, class_of_next, data_to_next = path(
                scroll_dict_empty, curr_position, curr_column, curr_row,
                right_class, center_class, left_class, class_of_next
            )

            print("Next position:", curr_position)
            print("Class:", class_of_next)

    # -------- EXIT --------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------ CLEANUP ------------------
for cap in [cap1, cap2, cap3]:
    if cap:
        cap.release()

cv2.destroyAllWindows()