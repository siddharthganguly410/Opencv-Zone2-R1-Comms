import cv2
import mediapipe as mp
import time
import math


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.65, min_tracking_confidence=0.7,static_image_mode=True)
mp_draw = mp.solutions.drawing_utils
send_interval = 0.5

cap = cv2.VideoCapture(0)

def detect_thumb_gesture(hand_landmarks):
    index_tip = hand_landmarks.landmark[8]
    index_mcp = hand_landmarks.landmark[5]

    dx = index_tip.x - index_mcp.x
    dy = index_tip.y - index_mcp.y

    angle = math.degrees(math.atan2(dy, dx))

    if angle < 0:
        angle += 360


    if 225 <= angle < 315:      
        return 1
    elif 315 <= angle or angle < 45:   
        return 2
    elif 45 <= angle < 135:
        return 3
    elif 135 <= angle < 225:
        return 4
    else:
        return 0

last_time = time.time()
last_gesture = -1
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture = 0
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = detect_thumb_gesture(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, str(gesture), (w - 100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
    print(gesture)


    cv2.imshow("Thumb Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()