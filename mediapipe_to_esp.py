import cv2                 # OpenCV for camera access and image processing
import mediapipe as mp      # MediaPipe for hand landmark detection
import socket               # Socket library for communication with ESP32
import time                 # Time library for controlling sending intervals
import math                 # Math for angle calculations

# ESP32 device details (change IP & port according to your ESP32)

ESP32_IP = "192.168.168.70"   # ESP32 IP address (should match your ESP32 WiFi network setup)
PORT = 5000                 # Port number (ESP32 should listen on the same port)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,                    # Detect only o ne hand
    min_detection_confidence=0.6,       # Minimum confidence for hand detection
    min_tracking_confidence=0.9,        # Minimum confidence for landmark tracking
    static_image_mode=False             # False = better for real-time video (tracking mode)
)

# Utility function for drawing landmarks
mp_draw = mp.solutions.drawing_utils

# Time interval for sending gestures to ESP32 (in seconds)
send_interval = 0.5

# Start webcam
cap = cv2.VideoCapture(0)


# Function to detect finger pointing direction using index finger landmarks
def detect_thumb_gesture(hand_landmarks):
    # Index finger tip and base landmarks
    index_tip = hand_landmarks.landmark[8]
    index_mcp = hand_landmarks.landmark[5]

    # Calculate difference in coordinates
    dx = index_tip.x - index_mcp.x
    dy = index_tip.y - index_mcp.y

    # Calculate angle (in degrees) using arctan2
    angle = math.degrees(math.atan2(dy, dx))

    # Normalize angle to range [0, 360)
    if angle < 0:
        angle += 360

    # Determine direction based on angle
    if 225 <= angle < 315:        # up
        return 1
    elif 315 <= angle or angle < 45:  # Right
        return 2
    elif 45 <= angle < 135:       # down
        return 3
    elif 135 <= angle < 225:      # Left
        return 4
    else:
        return 0                  # Default/unknown


# Keep track of last time we sent a command, and last gesture
last_time = time.time()
last_gesture = -1

# Main loop
while True:
    ret, frame = cap.read()    # Capture frame

    frame = cv2.flip(frame, 1) # Mirror image (selfie view)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert BGR → RGB (needed for MediaPipe)
    result = hands.process(rgb_frame) # Detect hand landmarks

    gesture = 0  # Default gesture
    if result.multi_hand_landmarks: # If hand detected
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = detect_thumb_gesture(hand_landmarks) # Detect gesture
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) # Draw landmarks

    # Show gesture number on screen
    cv2.putText(frame, str(gesture), (w - 100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

    print(gesture)  # Print gesture in console

    # Send gesture to ESP32 every 0.5s (if gesture changed)
    if (time.time() - last_time >= send_interval) and (gesture != last_gesture):
        try:
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ESP32_IP, PORT))   # Connect to ESP32
            s.send(str(gesture).encode()) # Send gesture as string (encoded to bytes)
            s.close()
            print(f"Sent: {gesture}")     # Debug print
        except Exception as e:
            print(f"Error sending {gesture}: {e}") # Handle errors
        last_gesture = gesture            # Update last gesture

    # Show video feed with landmarks and gesture
    cv2.imshow("Thumb Gesture Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Before quitting, send "0" to stop robot/device
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ESP32_IP, PORT))
        s.send(str(0).encode())
        s.close()
        print(f"Sent: {0}")
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()