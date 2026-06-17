# from ultralytics import YOLO
# import cv2
# model=YOLO('best.pt')
# cap=cv2.VideoCapture(0)

# while True:
#     ret,frame=cap.read()
#     if not ret:
#         break
#     results=model.predict(source=frame,conf=0.6,verbose=False)
#     for result in results:
#         annotated_frame=result.plot()
    
#     cv2.imshow('Spearhead',annotated_frame)

#     if cv2.waitKey(1) & 0xFF==ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# from ultralytics import YOLO
# import cv2

# model = YOLO('spearhead_palm3.pt').to('cuda')

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = model.predict(
#         frame,
#         conf=0.5,
#         device=0,
#         verbose=False
#     )

#     for result in results:
#         frame = result.plot()

#     cv2.imshow("Spearhead", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
