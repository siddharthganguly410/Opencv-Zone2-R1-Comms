# main.py
import cv2
import numpy as np
from ultralytics import YOLO

from zone2_leftDetect import process_left as ld
from zone2_rightDetect import process_right as rd
from zone2_centerDetect import process_center as cd
from zone2_path import path

process_zone1 = False
zone1_angle = None
zone1_xc = None
zone1_yc = None

FRAME_WIDTH = 640
CAM_FOV = 80

# Load YOLO models
model = YOLO("symbol240_9.pt")
model2 = YOLO("spf3.pt")

# Camera initialization
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

# Navigation / state variables
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
scroll_dict_empty = {
    1: scroll_list[0], 2: scroll_list[0], 3: scroll_list[0],
    4: scroll_list[0], 5: scroll_list[0], 6: scroll_list[0],
    7: scroll_list[0], 8: scroll_list[0], 9: scroll_list[0],
    10: scroll_list[0], 11: scroll_list[0], 12: scroll_list[0]
}

while True:
    ret1, f1 = cap1.read()
    ret2, f2 = cap2.read()

    if not ret1 or not ret2:
        break

    key = cv2.waitKey(1) & 0xFF

    # # Color thresholds
    # lower_green = np.array([140, 240, 127])
    # upper_green = np.array([146, 255, 133])

    # lower_red = np.array([90, 33, 240])
    # upper_red = np.array([118, 58, 255])

    # YOLO inference
    results1 = model.predict(f1, conf=0.8, device=0, verbose=False)
    results2 = model.predict(f2, conf=0.8, device=0, verbose=False)

    # Draw grid lines
    cv2.line(f1, (0, 160), (640, 160), (255, 0, 0), 1)
    cv2.line(f2, (0, 160), (640, 160), (255, 0, 0), 1)

    cv2.line(f1, (0, 320), (640, 320), (255, 0, 0), 1)
    cv2.line(f2, (0, 320), (640, 320), (255, 0, 0), 1)

    cv2.line(f1, (320, 0), (320, 480), (255, 0, 0), 1)  # VERTICAL CENTER LINE
    cv2.line(f2, (320, 0), (320, 480), (255, 0, 0), 1)  # VERTICAL CENTER LINE

    # Plot YOLO detections
    for result1 in results1:
        f1 = result1.plot()

    for result2 in results2:
        f2 = result2.plot()

    # Display feeds
    cv2.imshow("Left", f1)
    cv2.imshow("Right", f2)

    # Path update (L key)
    if key == ord('l'):
        right_class, pos1 = rd(results2, f2, model)
        left_class, pos2 = ld(results1, f1, model)
        center_class = cd(pos1, pos2)

        for i in scroll_dict_empty:
            if scroll_dict_empty[i] == "Empty" and i in (1, 2, 3):
                scroll_dict_empty[1] = right_class
                scroll_dict_empty[2] = center_class
                scroll_dict_empty[3] = left_class

        print("Current Position : ",curr_position[0])
        curr_position, curr_column, class_of_next, data_to_next = path(
            scroll_dict_empty,
            curr_position,
            curr_column,
            curr_row,
            right_class,
            center_class,
            left_class,
            class_of_next
        )
        print("Next Position:",curr_position[0])
        print("Class of Next :",class_of_next)
        # print("Data : ",data_to_next)

    # Next position (R key)
    if key == ord('r'):
        right_class, pos1 = rd(results2, f2, model)
        left_class, pos2 = ld(results1, f1, model)
        center_class = cd(pos1, pos2)

        curr_position, curr_column, class_of_next, data_to_next = path(
            scroll_dict_empty,
            curr_position,
            curr_column,
            curr_row,
            right_class,
            center_class,
            left_class,
            class_of_next
        )

        print("Next_position :", curr_position[0])
        # print("Next_Column", curr_column)
        # print("Data :", data_to_next)
        print("Class of next :", class_of_next)
        # print(scroll_dict_empty)

    if key == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
