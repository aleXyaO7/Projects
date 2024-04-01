import cv2
from face_mesh import FaceMeshDetector
from drowsiness_alerter import DrowsinessAlerter
import requests
from playsound import playsound

class VideoCamera(object):
    def __init__(self):
        self.face_mesh_detector = FaceMeshDetector()
        self.drowsiness_alerter = DrowsinessAlerter()
        self.drowsy = False
        self.drowsiness_counter = 0
        # Find the first available working webcam
        camera_feed_val = 0
        while camera_feed_val < 5:
            self.video = cv2.VideoCapture(camera_feed_val)
            try:
                ret, frame = self.video.read()
                ret, jpeg = cv2.imencode(".jpg", frame)
                break
            except:
                camera_feed_val += 1
        if camera_feed_val >= 5:
            raise Exception("No functioning video camera.")
    
    def __del__(self):
        self.video.release()

    def report_drowsy(self):
        # send a POST request to the backend
        # parameters: latitude, longitude, time
        body = '{"hello world"}'
        print("body ",body)
        req = requests.post("http://127.0.0.1:5001", data=body)

    def get_frame(self):
        ret, frame = self.video.read()
        frame, is_drowsy = self.face_mesh_detector.detect_mesh(frame)
        alert_sent = self.drowsiness_alerter.should_alert(is_drowsy)
        if alert_sent:
            self.generate()
        #print(is_drowsy)
        self.drowsy = is_drowsy
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
    
    def generate(self):
        sounds = {
            #0: "sounds/airhorn.mp3",
            #0: "sounds/Alice_wake_up.wav",
            #1: "sounds/Alice_wake_up.wav"
            0: "youshouldgetsomerest.mp3"
        }
        playsound(sounds[0])
        #playsound(sounds[1])


        