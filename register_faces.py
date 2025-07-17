import os
import cv2
import pickle
import numpy as np
import mediapipe as mp

FACE_FOLDER = 'static/faces'
ENCODING_FILE = 'data/encodings.pkl'

def get_face_vector(image):
    mp_face = mp.solutions.face_mesh
    with mp_face.FaceMesh(static_image_mode=True) as face_model:
        result = face_model.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0]
            return np.array([[pt.x, pt.y, pt.z] for pt in landmarks.landmark]).flatten()
    return None

def create_encodings():
    face_data = {}
    for person_name in os.listdir(FACE_FOLDER):
        person_path = os.path.join(FACE_FOLDER, person_name)
        if not os.path.isdir(person_path):
            continue

        vectors = []
        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            image = cv2.imread(image_path)
            vector = get_face_vector(image)
            if vector is not None:
                vectors.append(vector)

        if vectors:
            face_data[person_name] = np.mean(vectors, axis=0)

    with open(ENCODING_FILE, 'wb') as file:
        pickle.dump(face_data, file)
    print("Encodings saved successfully.")

if __name__ == "__main__":
    create_encodings()
