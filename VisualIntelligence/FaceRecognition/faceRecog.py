import os
import json
import time
import face_recognition
import cv2
from collections import deque

KNOWN_FACES_DIR = r"VisualIntelligence/known_faces/"
RECOGNIZED_FACES_QUEUE = deque(maxlen=5)
RELOAD_INTERVAL = 30  # seconds

# Ensure the known faces directory exists.
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Global cache variables.
_cached_face_encodings = []
_cached_face_names = []
_last_reload_time = 0

def load_known_faces():
    """
    Load known face encodings and names from the known_faces directory.
    Reload only if more than RELOAD_INTERVAL seconds have passed.
    """
    global _cached_face_encodings, _cached_face_names, _last_reload_time

    current_time = time.time()
    if (current_time - _last_reload_time) > RELOAD_INTERVAL or not _cached_face_encodings:
        print("Reloading known faces...")
        _cached_face_encodings = []
        _cached_face_names = []
        try:
            for image_name in os.listdir(KNOWN_FACES_DIR):
                if image_name.lower().endswith(('jpg', 'jpeg', 'png')):
                    image_path = os.path.join(KNOWN_FACES_DIR, image_name)
                    image = face_recognition.load_image_file(image_path)
                    face_encodings_in_image = face_recognition.face_encodings(image)
                    if face_encodings_in_image:
                        _cached_face_encodings.append(face_encodings_in_image[0])
                        _cached_face_names.append(os.path.splitext(image_name)[0])
        except Exception as e:
            print(f"Error loading known faces: {e}")
        _last_reload_time = current_time

    return _cached_face_encodings, _cached_face_names

def recognize_faces(frame):
    """
    Recognize faces in the frame and update recognized faces queue.
    """
    try:
        known_face_encodings, known_face_names = load_known_faces()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        recognized_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            RECOGNIZED_FACES_QUEUE.append(name)
            recognized_names.append(name)

        # Save the recognized faces to file
        with open("VisualIntelligence/currentface.txt", "w") as file:
            for name in RECOGNIZED_FACES_QUEUE:
                file.write(f"{name}\n")

        # If all recognized faces are unknown, take a snapshot.
        if all(name == "Unknown" for name in RECOGNIZED_FACES_QUEUE):
            snapshot_filename = os.path.join(KNOWN_FACES_DIR, "stranger.jpg")
            cv2.imwrite(snapshot_filename, frame)
            print(f"All faces unknown. Snapshot saved as {snapshot_filename}")
            RECOGNIZED_FACES_QUEUE.clear()

        return recognized_names

    except Exception as e:
        print(f"Error in face recognition: {e}")
        return []

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        recognize_faces(frame)
        cv2.imshow("Live Video Analysis", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
