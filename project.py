import cv2
import mediapipe as mp
import random
import math
from collections import deque

# Initialize Mediapipe Hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Snake Game variables
snake = deque()
snake_length = 10
food = None
score = 0

# Generate random food position
def new_food(width, height):
    return [random.randint(50, width - 50), random.randint(50, height - 50)]

# Distance helper
def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Main game
def play_snake():
    global snake, snake_length, food, score

    cap = cv2.VideoCapture(0)
    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)

    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    food = new_food(width, height)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Index fingertip = landmark 8
                x = int(hand_landmarks.landmark[8].x * width)
                y = int(hand_landmarks.landmark[8].y * height)
                point = [x, y]

                # Add head to snake
                snake.append(point)
                if len(snake) > snake_length:
                    snake.popleft()

                # Check collision with food
                if dist(point, food) < 25:
                    score += 1
                    snake_length += 5
                    food = new_food(width, height)

                # Draw snake
                for i in range(1, len(snake)):
                    cv2.line(frame, tuple(snake[i - 1]), tuple(snake[i]), (0, 255, 0), 15)
                cv2.circle(frame, tuple(point), 10, (0, 0, 255), -1)

                # Draw food
                cv2.circle(frame, tuple(food), 10, (255, 0, 0), -1)

                # Draw score
                cv2.putText(frame, f"Score: {score}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Self collision detection
                if len(snake) > 10:
                    for i in range(len(snake) - 10):
                        if dist(point, snake[i]) < 10:
                            cv2.putText(frame, "GAME OVER", (200, 250),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                            cv2.imshow("Snake Game", frame)
                            cv2.waitKey(3000)
                            cap.release()
                            cv2.destroyAllWindows()
                            return

                # Draw hand landmarks (optional)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Snake Game", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    play_snake()
