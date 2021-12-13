from flask import Response, Flask, render_template
import simplejpeg
import os
import time
import threading
import cv2
from .constants import (
    cam_passes, desired_fps, cam_ips, width,
    height, base_ip, host, port, debug
)


# Array of the Camera Streams
camera_streams = []


class CameraStream():
    """
    Class to contain camera stream
    """

    def __init__(self, _url):
        self.output_frame = None
        self.lock = threading.Lock()
        source = _url
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FPS, desired_fps)
        time.sleep(2.0)
        self.prev_time = time.time()
        self.new_time = self.prev_time

    def stream(self, framerate=10):
        if self.cap.isOpened():
            while True:
                _, frame = self.cap.read()
                if frame.shape:
                    frame = cv2.resize(frame, (width, height))
                    self.new_time = time.time()
                    self.fps = int(1/(self.new_time-self.prev_time))
                    self.prev_time = self.new_time
                    cv2.putText(
                        frame, 
                        "FPS: " + str(self.fps),
                        (int(frame.shape[1]*4/5), frame.shape[0] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 2)
                    with self.lock:
                        self.output_frame = frame.copy()
                else:
                    continue 
        else:
            print('camera open failed')

    def generate(self):    
        while True:
            with self.lock:
                if self.output_frame is None:
                    continue
                encodedImage = simplejpeg.encode_jpeg(self.output_frame, colorspace='BGR')
                #if not flag:
                #    continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                  bytearray(encodedImage) + b'\r\n')

    def close(self):
        self.cap.release()


## Creating template directory to hold index.html in
template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'templates')
app = Flask(__name__, template_folder="/home/pi/templates")

def get_urls():
    ## I used nmap to auto get IP address from network
    ## whose names started with F (as all EZVIZ cameras do)
    ## If you know your own cam IP Addresses, replaces the lines
    ## array with tuples of (camera_id, camera_ip)
    ## Where cam_id is same as in your password dictionary above
    global camera_streams
    camera_streams = []
    if not cam_ips:
        lines = os.popen("sudo nmap -sn {}/24 | grep -E 'F[0-9]{8}'"
                        .format(base_ip)).readlines()
        lines = [line[21:-3].replace("(", "").split(" ") for line in lines]
        for cam_id, cam_ip in lines:
            cam_ips[cam_id] = cam_ip

    for cam_id, cam_ip in cam_ips.items():
        cam_pass = cam_passes[cam_id]
        camera_streams.append(
            CameraStream("rtsp://admin:{}@{}:554/h264_stream".fromat(
                cam_pass, cam_ip
            ))
        )

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

@app.route("/video_feed")
def video_feed1():
    if len(camera_streams) > 0:
        return Response(camera_streams[0].generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    return"<h1>Not yet available</h1>"

@app.route("/video_feed2")
def video_feed2():
    if len(camera_streams) > 1:
        return Response(camera_streams[1].generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    return"<h1>Not yet available</h1>"

@app.route("/video_feed3")
def video_feed3():
    if len(camera_streams) > 2:
        return Response(camera_streams[2].generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    return"<h1>Not yet available</h1>"

@app.route("/video_feed4")
def video_feed4():
    if len(camera_streams) > 3:
        return Response(camera_streams[3].generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")
    return"<h1>Not yet available</h1>"


# check to see if this is the main thread of execution
if __name__ == '__main__':
    get_urls()

    for cam in camera_streams:
        t = threading.Thread(target=cam.stream, args=(3,))
        t.daemon = True
        t.start()
 
    # start the flask app
    app.run(host=host, port=port, debug=debug,
        threaded=True, use_reloader=False)
 
# release the video stream pointer
cv2.destroyAllWindows()
for cam in camera_streams:
    cam.close()
