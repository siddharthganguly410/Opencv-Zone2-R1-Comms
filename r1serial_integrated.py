import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import serial
import time

# Shared camera
cap = cv2.VideoCapture(0)

# Shared variable for tag display
current_tag = None
lock = threading.Lock()


# def serial_thread():
#     global current_tag

#     ser = serial.Serial('COM3', 115200)
#     time.sleep(2)
#     print("Serial thread started...")

#     while True:
#         if ser.in_waiting > 0:
#             cmd = ser.readline().decode().strip()
#             print("Received:", cmd)
#             with lock:
#                 if cmd == 'ready':
#                     current_tag = cv2.imread('atag0.png')

#                 elif cmd == 'next':
#                     current_tag = cv2.imread('atag1.png')

#                 elif cmd == 'prev':
#                     current_tag = cv2.imread('atag2.png')

def keyboard_thread():
    global current_tag

    print("Keyboard control:")
    print("r = ready | n = next | p = prev | q = quit")

    while True:
        key = input("Enter command: ").strip()
                                                                        
        with lock:
            if key == 'r':
                current_tag = cv2.imread('atag0.png')
            elif key == 'n':
                current_tag = cv2.imread('atag1.png')
            elif key == 'p':
                current_tag = cv2.imread('atag2.png')
            elif key == 'q':
                break

class VideoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_tag

        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        oldtime = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # FPS calculation
            newtime = time.time()
            fps = 1 / (newtime - oldtime) if oldtime != 0 else 0
            oldtime = newtime

            frame = cv2.putText(frame, f"FPS: {int(fps)}",
                                (20, 40),
                                cv2.FONT_HERSHEY_DUPLEX,
                                1,
                                (255, 0, 0),
                                2)

            # Overlay tag if available
            with lock:
                if current_tag is not None:
                    tag_resized = cv2.resize(current_tag, (150, 150))
                    frame[10:160, 10:160] = tag_resized

            _, jpeg = cv2.imencode('.jpg', frame)

            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(jpeg.tobytes())
            self.wfile.write(b'\r\n')

# -------------------- MAIN --------------------
def start_server():
    server = HTTPServer(('192.168.29.202', 8080), VideoHandler)
    print("Streaming on http://<jetson-ip>:8080")
    server.serve_forever()

# Start threads
# t1 = threading.Thread(target=serial_thread, daemon=True)   SERIAL 
t1 = threading.Thread(target=keyboard_thread, daemon=True) # NON-SERIAL
t1.start()

t2 = threading.Thread(target=start_server)
t2.start()

t2.join()