import mediapipe as mp
import cv2
'''
cap=cv2.VideoCapture(0)
while cap.isOpened():
    ret,frame=cap.read()
    cv2.imshow('wc',frame)

    if cv2.waitKey(5) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

mp_drawing=mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic
cap=cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret,frame=cap.read()
        img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=holistic.process(img)
        #img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(frame,results.face_landmarks,mp_holistic.FACEMESH_TESSELATION)
        mp_drawing.draw_landmarks(frame,results.right_hand_landmarks,mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(frame,results.left_hand_landmarks,mp_holistic.HAND_CONNECTIONS)
        #mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS)
        cv2.imshow('Holistic',frame)

        if cv2.waitKey(10)     & 0xFF==ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


