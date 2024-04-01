from flask import Flask, render_template, Response, request, jsonify
from camera import VideoCamera
import pandas as pd

#from webservices import app_webservices
global_msg = ""
app = Flask(__name__)

@app.route("/")
def index():
    # rendering webpage
    return render_template("index.html")

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        global_msg = camera.drowsy
        #drowsy = camera.get_frame2()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    s = VideoCamera()
    resp = Response(gen(s),
                mimetype="multipart/x-mixed-replace; boundary=frame")#,
    return resp

@app.route("/get-data",methods=['GET'])
def get_data(msg = global_msg):
    #print("msg: ",msg)
    data = msg
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port="5001", debug=True)