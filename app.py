import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, Response
from helpers import load_saved_encodings, compare_faces, mark_attendance, read_attendance

app = Flask(__name__)
known_faces = load_saved_encodings()

mp_face = mp.solutions.face_mesh
face_model = mp_face.FaceMesh(static_image_mode=False)

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break

        result = face_model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if result.multi_face_landmarks:
            for landmarks in result.multi_face_landmarks:
                face_vector = np.array([[pt.x, pt.y, pt.z] for pt in landmarks.landmark]).flatten()
                name = compare_faces(face_vector, known_faces)

                if name != "Unknown":
                    mark_attendance(name)

                h, w = frame.shape[:2]
                x = int(landmarks.landmark[1].x * w)
                y = int(landmarks.landmark[1].y * h)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin')
def admin():
    logs = read_attendance()
    return render_template('admin.html', logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
