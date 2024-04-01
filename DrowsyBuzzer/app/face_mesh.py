import mediapipe as mp
import cv2
from scipy.spatial import distance

class FaceMeshDetector:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.eye_landmarks = [33, 133, 160, 144, 158, 153, 362, 263, 385, 380, 387, 373]

    def get_eye_aspect_ratio(self, eye_landmarks):
        horizontal = distance.euclidean(eye_landmarks[0], eye_landmarks[1])
        vertical_1 = distance.euclidean(eye_landmarks[2], eye_landmarks[3])
        vertical_2 = distance.euclidean(eye_landmarks[4], eye_landmarks[5])
        ear = (vertical_1 + vertical_2) / (2* horizontal)
        return ear

    def detect_mesh(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        is_drowsy = False
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark_coords = [(d.x, d.y, d.z) for d in face_landmarks.landmark]
                
                # self.mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_tesselation_style()
                # )

            eye_coords = [(landmark_coords[index][0],landmark_coords[index][1]) for index in self.eye_landmarks]

            #image = self.draw_eye_lines(image, eye_coords)

            drowsiness, ear_right, ear_left = self.get_drowsiness_level(eye_coords)

            is_drowsy = drowsiness < 0.3

            #image = self.display_drowsiness(image, is_drowsy, ear_right, ear_left)
            image = self.display_drowsiness(image, is_drowsy)

        return image, is_drowsy

    def display_drowsiness(self, image, is_drowsy):
        status = "Drowsy" if is_drowsy else "Awake"
        cv2.putText(image, status, org=(200,100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0,0,0), thickness=2)
        return image


    def get_drowsiness_level(self, eye_coords):
        ear_right = self.get_eye_aspect_ratio(eye_coords[:6])
        ear_left = self.get_eye_aspect_ratio(eye_coords[6:])
        drowsiness = (ear_right + ear_left) / 2
        return drowsiness, ear_right, ear_left