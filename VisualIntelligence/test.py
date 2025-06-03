import cv2
import concurrent.futures
import keyboard
import threading
import tkinter as tk
import numpy as np

from FaceRecognition.faceRecog import recognize_faces
from ObjectDetection.ObjectDetection import describtion
from Gesture_recognition.gestrcg import gestrecog
from Gesture_recognition.eyestracker import run_eye_tracker  # Corrected eye tracker import
# from FaceRecognition.mood_detection import detect_mood

OUTPUT_FILE = "VisualIntelligence/output.txt"

exit_flag = threading.Event()
selection_event = threading.Event()
selected_mode = None

def listen_for_hotkey():
    while True:
        keyboard.wait('ctrl+alt+g')
        exit_flag.set()          # Stop current camera loop
        threading.Thread(target=show_mode_selector, daemon=True).start()

def analyze_live_video():
    cap = cv2.VideoCapture(0)
    exit_flag.clear()

    while cap.isOpened() and not exit_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_faces = executor.submit(recognize_faces, frame)
            future_objects = executor.submit(describtion, frame)

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

def Gesture_recognition():
    gestrecog()

def Eye_tracker():
    run_eye_tracker()

def show_mode_selector():
    global selected_mode

    def select_mode(mode):
        global selected_mode
        selected_mode = mode
        root.destroy()
        selection_event.set()

    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)  # Always on top
    root.configure(bg='white', bd=0, highlightthickness=0)
    root.geometry("450x450+1470+30")  # Circular window size (450x450)

    # Create a Canvas widget to make the window round and manage transparency
    canvas = tk.Canvas(root, width=450, height=450, bg='white', bd=0, highlightthickness=0)
    canvas.pack()

    # Draw a circular background with a blue border and white center
    canvas.create_oval(10, 10, 440, 440, fill='white', outline="#4169E1", width=4)  # Blue border, white fill

    # Create buttons in a circular layout like a weapon wheel
    num_buttons = 3
    button_radius = 120  # Radius of the circular layout
    button_labels = ["Analyze", "Gesture", "Eye Tracker"]

    for i, label in enumerate(button_labels):
        angle = i * (360 / num_buttons)  # Angle for each button
        x_pos = 225 + button_radius * np.cos(np.radians(angle))  # X position based on angle
        y_pos = 225 + button_radius * np.sin(np.radians(angle))  # Y position based on angle
        button = tk.Button(root, text=label, font=('Helvetica', 14), command=lambda mode=label: select_mode(mode), bg='white', fg="#4169E1", relief="flat")
        button.place(x=x_pos, y=y_pos, width=120, height=40)

    # Set the window shape to match the circular design (using wm_geometry and canvas)
    root.after(100, lambda: root.geometry('450x450+1470+30'))  # Ensure circular shape is set

    root.mainloop()

def main():
    global selected_mode
    current_mode = "analyze"

    # Start the hotkey listener
    threading.Thread(target=listen_for_hotkey, daemon=True).start()

    while True:
        if current_mode == "analyze":
            analyze_live_video()
        elif current_mode == "gesture":
            Gesture_recognition()
        elif current_mode == "eye_tracker":
            Eye_tracker()

        print("\nPress Ctrl+Alt+G to open mode selector, or Esc to exit.")
        while True:
            if selection_event.is_set():
                current_mode = selected_mode
                selected_mode = None
                selection_event.clear()
                print(f"Switched to {current_mode} mode.")
                break
            elif keyboard.is_pressed('esc'):
                print("Exiting program...")
                return

if __name__ == "__main__":
    main()
