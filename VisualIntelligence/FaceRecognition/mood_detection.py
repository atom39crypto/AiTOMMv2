import cv2  # Ensure OpenCV is installed: pip install opencv-python
import json
import os
import tempfile
from collections import deque, Counter
from deepface import DeepFace  # Ensure DeepFace is installed: pip install deepface

CACHE_FILE = os.path.join(tempfile.gettempdir(), "VisualIntelligence/FaceRecognition/emotion_cache.json")
MAX_CACHE = 10
SMOOTHING_WINDOW = 10  # Number of frames to smooth emotions

# Load existing emotion cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as file:
        try:
            emotion_cache = deque(json.load(file), maxlen=MAX_CACHE)
        except json.JSONDecodeError:
            emotion_cache = deque(maxlen=MAX_CACHE)
else:
    emotion_cache = deque(maxlen=MAX_CACHE)

# Initialize emotion smoothing queue
emotion_history = deque(maxlen=SMOOTHING_WINDOW)

def detect_mood(frame):
    """Detects and smooths emotions over multiple frames."""
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        detected_emotion = analysis[0]['dominant_emotion']
    except:
        detected_emotion = "Unknown"

    # Store detected emotions for smoothing
    emotion_history.append(detected_emotion)

    # Compute the most consistent mood using weighted emotion count
    if len(emotion_history) >= SMOOTHING_WINDOW:
        emotion_counts = Counter(emotion_history)
        mood = max(emotion_counts, key=lambda x: emotion_counts[x] * (1 + 0.1 * emotion_history.count(x)))
    else:
        mood = detected_emotion

    # Maintain a stack of the last 5 moods
    emotion_cache.append(mood)

    # Save the stack to a file
    with open('VisualIntelligence\\FaceRecognition\\local_cache\\emotion.txt', "w") as file:
        file.write("\n".join(emotion_cache))
    return mood

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    last_capture_time = 0
    interval = 1 / 2.5  # 5 FPS = every 0.2 seconds

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        mood = detect_mood(frame)  # Get detected mood


            # Display results on the video feed
        cv2.putText(frame, f"Mood: {mood}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Live Video Analysis", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()