# import cv2
# from flask import Flask, Response, render_template

# app = Flask(__name__)
# cap = cv2.VideoCapture(0)  # 0 = default webcam

# def generate_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             # Encode frame as JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # MJPEG format
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='10.0.59.148', port=5000, debug=True)
# import cv2
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time
# class VideoHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
#         self.end_headers()

#         cap = cv2.VideoCapture(0)
#         oldtime=0
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 continue
#             newtime=time.time()
#             fps=1/(newtime-oldtime)
#             oldtime=newtime
#             fps=str(fps)
#             frame=cv2.putText(frame,fps,(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2,cv2.LINE_AA)
#             cv2.line(frame,(320,0),(320,480),(255,0,0),1)
#             cv2.line(frame,(0,240),(640,240),(255,0,0),1)
#             _, jpeg = cv2.imencode('.jpg', frame)

#             self.wfile.write(b'--frame\r\n')
#             self.send_header('Content-Type', 'image/jpeg')
#             self.end_headers()
#             self.wfile.write(jpeg.tobytes())
#             self.wfile.write(b'\r\n')

# server = HTTPServer(('172.21.175.204', 8080), VideoHandler)
# print("Streaming on http://<jetson-ip>:8080")
# server.serve_forever()
import cv2
from flask import Flask, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            height, width, _ = frame.shape

            center_x = width // 2
            center_y = height // 2

            cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)
            cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "<h2>Jetson Camera Stream with Grid</h2><img src='/video'>"

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)