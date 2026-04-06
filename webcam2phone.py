import cv2
from flask import Flask, Response, render_template
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    oldtime = time.time()   # FIX: initialize inside function

    while True: 
        success, frame = camera.read()
        if not success:
            break

        # Calculate FPS
        newtime = time.time()
        fps = 1 / (newtime - oldtime)
        oldtime = newtime

        fps_text = f"FPS: {int(fps)}"

        # Put text BEFORE encoding
        cv2.putText(frame, fps_text, (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1,
                    (255, 0, 0), 2, cv2.LINE_AA)
        cv2.line(frame,(320,0),(320,480),(255,0,0),1)
        cv2.line(frame,(0,240),(640,240),(255,0,0),1)
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Stream frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='172.21.175.204', port=5000, debug=True)