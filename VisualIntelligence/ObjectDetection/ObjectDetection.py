import time
import cv2
import torch
import numpy as np
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def preprocess_image(image):
    """Preprocess image for better OCR accuracy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def describe_image(image):
    """Generate a natural language description of an image."""
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    inputs = processor(pil_image, return_tensors="pt")
    
    with torch.no_grad():
        output = model.generate(**inputs, max_length=75)

    description = processor.batch_decode(output, skip_special_tokens=True)[0]


    return description

def describtion(frame):
    last_capture_time = 0
    interval = 1 / 5  # 5 FPS = every 0.2 seconds
    OUTPUT_FILE = "VisualIntelligence/output.txt"
    current_time = time.time()
    if current_time - last_capture_time >= interval:
        last_capture_time = current_time
        frame_key = f"frame_{int(current_time * 1000)}"
        description = describe_image(frame)

        with open(OUTPUT_FILE, "w") as f:
            f.write(f"Frame: {frame_key}\n")
            f.write(f"Image Description: {description}\n")
            f.write("-" * 50 + "\n")


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        describtion(frame)

        # cv2.putText(frame, f"Text: {text[:30]}...", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Live Video Analysis", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    

    cap.release()
    cv2.destroyAllWindows()