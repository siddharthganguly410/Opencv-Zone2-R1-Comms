import cv2
import numpy as np

# ==========================
# CAMERA SETUP
# ==========================

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ==========================
# MAIN LOOP
# ==========================

while True:

    ret1, img1 = cam1.read()
    ret2, img2 = cam2.read()

    if not ret1 or not ret2:
        print("Camera read failed")
        break

    # =====================================
    # CAMERA 1 PROCESSING
    # =====================================

    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    # OpenCV HSV:
    # H: 0-179
    # S: 0-255
    # V: 0-255

    #RED MASK
    lower_red1 = np.array([0, 0, 0])
    upper_red1 = np.array([14, 255, 90])
    lower_red2 = np.array([165, 38, 51])
    upper_red2 = np.array([179, 255, 142])
    
    redMask1 = cv2.inRange(hsv1, lower_red1, upper_red1)
    redMask2 = cv2.inRange(hsv1, lower_red2, upper_red2)
    redMask=cv2.bitwise_or(redMask1,redMask2)
   # =====================================
    # RED
    # =====================================

    # lower_red = np.array([160, 70, 35])
    # upper_red = np.array([175, 255, 140])

    # redMask = cv2.inRange(
    #     hsv1,
    #     lower_red,
    #     upper_red
    # )

# =====================================
# BLUE
# =====================================

    lower_blue = np.array([95, 25, 20])
    upper_blue = np.array([135, 255, 180])

    blueMask = cv2.inRange(
        hsv1,
        lower_blue,
        upper_blue
    )
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (9, 9))

    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (21, 21))

    redMask = cv2.morphologyEx(
        redMask, cv2.MORPH_OPEN, kernel_open)

    redMask = cv2.morphologyEx(
        redMask, cv2.MORPH_CLOSE, kernel_close)

    blueMask = cv2.morphologyEx(
        blueMask, cv2.MORPH_OPEN, kernel_open)

    blueMask = cv2.morphologyEx(
        blueMask, cv2.MORPH_CLOSE, kernel_close)

    output1 = img1.copy()

    # RED OBJECTS
    contours, _ = cv2.findContours(
        redMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 3000:

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.6 < ratio < 1.4:

                cv2.rectangle(
                    output1,
                    (x, y),
                    (x+w, y+h),
                    (0, 0, 255),
                    4)

                cv2.putText(
                    output1,
                    "RED",
                    (x, max(20, y-10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2)

    # BLUE OBJECTS
    contours, _ = cv2.findContours(
        blueMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 3000:

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.6 < ratio < 1.4:

                cv2.rectangle(
                    output1,
                    (x, y),
                    (x+w, y+h),
                    (255, 0, 0),
                    4)

                cv2.putText(
                    output1,
                    "BLUE",
                    (x, max(20, y-10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2)

    # =====================================
    # CAMERA 2 PROCESSING
    # =====================================

    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    redMask1 = cv2.inRange(
        hsv2,
        np.array([0,25,64]),
        np.array([9,255,217]))

    redMask2 = cv2.inRange(
        hsv2,
        np.array([160,40,35]),
        np.array([179,255,180]))

    redMask = cv2.bitwise_or(
        redMask1,
        redMask2)

    # blueMask = cv2.inRange(
    #     hsv2,
    #     np.array([99,25,20]),
    #     np.array([135,255,153]))
    # =====================================
# RED
# =====================================

    # lower_red = np.array([160, 70, 35])
    # upper_red = np.array([175, 255, 140])

    # redMask = cv2.inRange(
    #     hsv2,
    #     lower_red,
    #     upper_red
    # )

# =====================================
# BLUE
# =====================================

    lower_blue = np.array([95, 25, 20])
    upper_blue = np.array([135, 255, 180])

    blueMask = cv2.inRange(
        hsv2,
        lower_blue,
        upper_blue
    )
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,(11,11))

    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,(25,25))

    redMask = cv2.morphologyEx(
        redMask, cv2.MORPH_OPEN, kernel_open)

    redMask = cv2.morphologyEx(
        redMask, cv2.MORPH_CLOSE, kernel_close)

    blueMask = cv2.morphologyEx(
        blueMask, cv2.MORPH_OPEN, kernel_open)

    blueMask = cv2.morphologyEx(
        blueMask, cv2.MORPH_CLOSE, kernel_close)

    output2 = img2.copy()

    # RED
    contours, _ = cv2.findContours(
        redMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 5000:

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.75 < ratio < 1.25:

                cv2.rectangle(
                    output2,
                    (x,y),
                    (x+w,y+h),
                    (0,0,255),
                    4)

                cv2.putText(
                    output2,
                    "RED",
                    (x,max(20,y-10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2)

    # BLUE
    contours, _ = cv2.findContours(
        blueMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 5000:

            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / float(h)

            if 0.75 < ratio < 1.25:

                cv2.rectangle(
                    output2,
                    (x,y),
                    (x+w,y+h),
                    (255,0,0),
                    4)

                cv2.putText(
                    output2,
                    "BLUE",
                    (x,max(20,y-10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,255),
                    2)

    # =====================================
    # DISPLAY
    # =====================================

    cv2.imshow("Camera 1", output1)
    cv2.imshow("Camera 2", output2)

    

    if cv2.waitKey(1) & 0xFF== ord('q'):      
        break

# =====================================
# CLEANUP
# =====================================

cam1.release()
cam2.release()

cv2.destroyAllWindows()