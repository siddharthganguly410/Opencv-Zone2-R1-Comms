# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         break

#     # Detect black color in BGR
#     lower = np.array([0, 0, 0])
#     upper = np.array([60, 60, 60])

#     # Black areas become WHITE in mask
#     mask = cv2.inRange(frame, lower, upper)
#     contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
#     if len(contours) > 0:
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
            
#             area=w*h
#             if 5000<=area<=15000:
#                 cv2.rectangle(mask, (x, y), (x+w, y+h), (255, 0, 0), 2)
#                 area=str(w*h)
#                 cv2.putText(mask,area,(w//2,h//2),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA,False)
#     cv2.imshow("Original", frame)
#     cv2.imshow("Black Mask", mask)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while True:

#     ret, frame = cap.read()

#     if not ret:
#         break

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # White edge detection
#     _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     contours, _ = cv2.findContours(
#         mask,
#         cv2.RETR_EXTERNAL,
#         cv2.CHAIN_APPROX_SIMPLE
#     )

#     for cnt in contours:

#         area = cv2.contourArea(cnt)

#         if area > 5000:

#             # Create filled contour mask
#             filled = np.zeros_like(gray)

#             cv2.drawContours(
#                 filled,
#                 [cnt],
#                 -1,
#                 255,
#                 thickness=cv2.FILLED
#             )

#             # Extract only inside region
#             inside = cv2.bitwise_and(gray, gray, mask=filled)

#             # Detect black area inside object
#             black_mask = cv2.inRange(inside, 0, 50)

#             inner_contours, _ = cv2.findContours(
#                 black_mask,
#                 cv2.RETR_EXTERNAL,
#                 cv2.CHAIN_APPROX_SIMPLE
#             )

#             if len(inner_contours) > 0:

#                 biggest = max(inner_contours, key=cv2.contourArea)

#                 x, y, w, h = cv2.boundingRect(biggest)

#                 # Draw rectangle INSIDE object
#                 cv2.rectangle(
#                     frame,
#                     (x, y),
#                     (x+w, y+h),
#                     (0, 0, 255),
#                     3
#                 )

#     cv2.imshow("Frame", frame)
#     cv2.imshow("Mask", mask)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import numpy as np
# cap=cv2.VideoCapture(0)
# while True:
#     ret,frame=cap.read()
#     if not ret:
#         break
#     gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     cv2.imshow('frame',frame)
#     cv2.imshow('gray',gray)
#     if cv2.waitKey(1) & 0xFF==ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()


