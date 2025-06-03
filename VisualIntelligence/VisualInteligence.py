import cv2
import concurrent.futures
import keyboard
import threading
import tkinter as tk
import time
import os
import sys

from FaceRecognition.faceRecog import recognize_faces
from ObjectDetection.ObjectDetection import describtion
from Gesture_recognition.gestrcg import gestrecog
from Gesture_recognition.eyestracker import run_eye_tracker

OUTPUT_FILE = "VisualIntelligence/output.txt"
MODE_FILE = "selected_mode.txt"  # File to store the selected mode

exit_flag = threading.Event()
selection_event = threading.Event()
selected_mode = "analyze"  # Default mode
cap = None  # Camera capture object

def switch_mode(mode):
    global selected_mode
    selected_mode = mode
    exit_flag.set()  # Stop the current mode
    save_selected_mode(mode)  # Save the selected mode
    restart_program()  # Trigger a full restart

def listen_for_hotkeys():
    keyboard.add_hotkey('ctrl+alt+a', lambda: switch_mode('analyze'))
    keyboard.add_hotkey('ctrl+alt+g', lambda: switch_mode('gesture'))
    keyboard.add_hotkey('ctrl+alt+e', lambda: switch_mode('eye_tracker'))
    keyboard.add_hotkey('ctrl+alt+m', lambda: threading.Thread(target=show_mode_selector, daemon=True).start())
    
    print("Global hotkeys registered: Ctrl+Alt+A/G/E/M")

    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting program...")
            os._exit(0)  # forcefully terminate everything
        time.sleep(0.1)

def analyze_live_video():
    global cap
    cap = cv2.VideoCapture(0)
    exit_flag.clear()
    while cap.isOpened() and not exit_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(recognize_faces, frame)
            executor.submit(describtion, frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()

def Gesture_recognition():
    exit_flag.clear()
    gestrecog()

def Eye_tracker():
    exit_flag.clear()
    run_eye_tracker()

def show_mode_selector():
    def select_mode(mode):
        switch_mode(mode)
        root.destroy()

    root = tk.Tk()
    root.title("Mode Selector")
    root.geometry("400x400+600+200")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg='black')

    canvas = tk.Canvas(root, width=400, height=400, bg='black', highlightthickness=0)
    canvas.pack()

    canvas.create_oval(50, 50, 350, 350, outline='white', width=3)

    tk.Button(root, text="Analyze", font=('Helvetica', 14), command=lambda: select_mode('analyze'), bg='white').place(x=160, y=80, width=80, height=40)
    tk.Button(root, text="Gesture", font=('Helvetica', 14), command=lambda: select_mode('gesture'), bg='white').place(x=80, y=250, width=100, height=40)
    tk.Button(root, text="Eye Tracker", font=('Helvetica', 14), command=lambda: select_mode('eye_tracker'), bg='white').place(x=220, y=250, width=100, height=40)

    root.mainloop()

def save_selected_mode(mode):
    with open(MODE_FILE, "w") as file:
        file.write(mode)

def load_selected_mode():
    if os.path.exists(MODE_FILE):
        with open(MODE_FILE, "r") as file:
            return file.read().strip()
    return "analyze"  # Default mode if the file doesn't exist

def main_loop():
    global selected_mode
    while True:
        print(f"\nStarting mode: {selected_mode}")
        if selected_mode == "analyze":
            analyze_live_video()
        elif selected_mode == "gesture":
            Gesture_recognition()
        elif selected_mode == "eye_tracker":
            Eye_tracker()

        print("Waiting for restart or exit...")
        while True:
            if exit_flag.is_set():
                break
            time.sleep(0.1)
        
        # Trigger the restart after mode switch
        print(f"Restarting {selected_mode} mode...")
        time.sleep(1)  # Give some time for the restart
        restart_program()

def restart_program():
    print("Restarting program...")
    # Reload the entire script to the beginning, passing the selected mode as an argument
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    selected_mode = load_selected_mode()  # Load the previously selected mode
    threading.Thread(target=listen_for_hotkeys, daemon=True).start()
    while True:
        main_loop()
