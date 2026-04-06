# main.py
import cv2
import numpy as np
from threading import Thread
from ultralytics import YOLO

from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd
from zone2_path import path

# ================= CAMERA THREAD CLASS =================
class Camera:
    def __init__(self, idx, width=640, height=480, fps=15):
        self.cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.ret, self.frame = self.cap.read()
        self.running = True

        Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.ret = ret
                self.frame = frame

    def read(self):
        return self.ret, self.frame

    def stop(self):
        self.running = False
        self.cap.release()


# ================= CONSTANTS =================
FRAME_WIDTH = 640
CAM_FOV = 80

process_zone1 = False
zone1_angle = None
zone1_xc = None
zone1_yc = None

curr_position = [0, 0]
curr_row = 0
curr_column = 0
data_to_next = 0

left_class = "Empty"
right_class = "Empty"
center_class = "Empty"
pos1 = "Empty"
pos2 = "Empty"
class_of_next = "Empty"

scroll_list = ["Empty", "R1 KFS", "R2 KFS", "Fake"]
scroll_dict_empty = {i: scroll_list[0] for i in range(1, 13)}

# ================= LOAD MODELS =================
model = YOLO("symbol240_9.pt")
model2 = YOLO("spf3.pt")

# ================= INIT CAMERAS =================
# IMPORTANT: indexes preserved from your code
cam_left   = Camera(2)
cam_right  = Camera(0)
cam_center = Camera(1)

# ================= MAIN LOOP =================
while True:
    r1, f1 = cam_left.read()
    r2, f2 = cam_right.read()
    r3, f3 = cam_center.read()

    if not (r1 and r2 and r3):
        print("Camera frame grab failed")
        break

    key = cv2.waitKey(1) & 0xFF

    # ================= HSV MASKS (ZONE 1) =================
    hsv3 = cv2.cvtColor(f3, cv2.COLOR_BGR2HSV)

    lower_green = np.array([140, 240, 127])
    upper_green = np.array([146, 255, 133])

    lower_red = np.array([90, 33, 240])
    upper_red = np.array([118, 58, 255])

    mask_green = cv2.inRange(hsv3, lower_green, upper_green)
    mask_red = cv2.inRange(hsv3, lower_red, upper_red)

    # ================= YOLO INFERENCE =================
    results1 = model(f1, conf=0.8, device=0, verbose=False)
    results2 = model(f2, conf=0.8, device=0, verbose=False)
    results3 = model2(f3, conf=0.8, device=0, verbose=False)

    # ================= DRAW GRID =================
    for img in (f1, f2):
        cv2.line(img, (0, 160), (640, 160), (255, 0, 0), 1)
        cv2.line(img, (0, 320), (640, 320), (255, 0, 0), 1)
        cv2.line(img, (320, 0), (320, 480), (255, 0, 0), 1)

    cv2.line(f3, (260, 0), (260, 480), (255, 0, 0), 1)
    cv2.line(f3, (380, 0), (380, 480), (255, 0, 0), 1)
    cv2.circle(f3, (320, 240), 3, (0, 255, 0), -1)

    # ================= PLOT RESULTS =================
    for r in results1:
        f1 = r.plot()
    for r in results2:
        f2 = r.plot()

    # ================= ZONE 1 ANGLE =================
    zone1_xc = zone1_yc = zone1_angle = None

    for r in results3:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            zone1_xc = (x1 + x2) // 2
            zone1_yc = (y1 + y2) // 2

            horizontal_offset = zone1_xc - 320
            zone1_angle = (horizontal_offset / FRAME_WIDTH) * CAM_FOV

    # ================= KEY CONTROLS =================
    if key == ord('z'):
        if zone1_xc is not None and 260 <= zone1_xc <= 380:
            print("YES")
            print("Angle:", zone1_angle)
            process_zone1 = True
        else:
            print("Next")
            process_zone1 = False

    elif key == ord('m') and process_zone1:
        if cv2.countNonZero(mask_green) > 0:
            print("REPEAT")
        elif cv2.countNonZero(mask_red) > 0:
            print("ZONE 2")

    if key == ord('l'):
        right_class, pos1 = rd(results2, f2, model)
        left_class, pos2 = ld(results1, f1, model)
        center_class = cd(pos1, pos2)

        scroll_dict_empty[1] = right_class
        scroll_dict_empty[2] = center_class
        scroll_dict_empty[3] = left_class

        curr_position, curr_column, class_of_next, data_to_next = path(
            scroll_dict_empty, curr_position, curr_column,
            curr_row, right_class, center_class, left_class, class_of_next
        )

        print("Current:", curr_position[0])
        print("Next class:", class_of_next)

    if key == ord('r'):
        right_class, pos1 = rd(results2, f2, model)
        left_class, pos2 = ld(results1, f1, model)
        center_class = cd(pos1, pos2)

        curr_position, curr_column, class_of_next, data_to_next = path(
            scroll_dict_empty, curr_position, curr_column,
            curr_row, right_class, center_class, left_class, class_of_next
        )

        print("Next position:", curr_position[0])
        print("Class of next:", class_of_next)

    # ================= DISPLAY =================
    for r in results3:
        f3 = r.plot()

    cv2.imshow("Left", f1)
    cv2.imshow("Right", f2)
    cv2.imshow("Zone 1", f3)

    if key == ord('q'):
        break

# ================= CLEANUP =================
cam_left.stop()
cam_right.stop()
cam_center.stop()
cv2.destroyAllWindows()
