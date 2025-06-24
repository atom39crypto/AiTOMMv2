import cv2
import json
import os
from collections import deque, Counter
from deepface import DeepFace

CACHE_FILE = "emotion_cache.json"

# Load existing cache (Keep only last 30 observations)
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as file:
        try:
            emotion_cache = deque(json.load(file), maxlen=30)
        except json.JSONDecodeError:
            emotion_cache = deque(maxlen=30)
else:
    emotion_cache = deque(maxlen=30)

cap = cv2.VideoCapture(0)

def get_mood():
    """Determine mood from the last few emotions using frequency analysis."""
    if not emotion_cache:
        return "Unknown"
    
    emotion_counts = Counter(entry["emotion"] for entry in emotion_cache)
    mood = emotion_counts.most_common(1)[0][0]  # Most frequent emotion
    return mood

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_hash = str(hash(frame.tobytes()))

    # Check if this frame is already cached
    emotion = None
    for entry in emotion_cache:
        if isinstance(entry, dict) and entry.get("hash") == frame_hash:
            emotion = entry["emotion"]
            break

    if not emotion:
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
            emotion_cache.append({"hash": frame_hash, "emotion": emotion})  # Store latest 30
            with open(CACHE_FILE, "w") as file:
                json.dump(list(emotion_cache), file)
        except:
            emotion = "Unknown"

    mood = get_mood()  # Determine overall mood

    # Display current frame's emotion and overall mood
    cv2.putText(frame, f"Emotion: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Mood: {mood}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Mood Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
