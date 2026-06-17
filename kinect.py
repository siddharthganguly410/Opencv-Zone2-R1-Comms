# # from pykinect2 import PyKinectRuntime
# # from pykinect2 import PyKinectV2

# # kinect = PyKinectRuntime.PyKinectRuntime(
# #     PyKinectV2.FrameSourceTypes_Color
# # )

# # print("Kinect connected")

# import cv2

# cap = cv2.VideoCapture(cv2.CAP_OPENNI2)

# if not cap.isOpened():
#     print("Cannot open Kinect")
#     exit()

# while True:
#     if cap.grab():
#         _, depth = cap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
#         _, color = cap.retrieve(cv2.CAP_OPENNI_BGR_IMAGE)

#         cv2.imshow("Depth", depth)
#         cv2.imshow("Color", color)

#     if cv2.waitKey(1) == 27:
#         break
import cv2

cap = cv2.VideoCapture(1)  # try 0,1,2,3...

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("Kinect RGB", frame)

    if cv2.waitKey(1) == 27:
        break