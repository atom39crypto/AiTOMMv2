import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import threading
import keyboard
import ctypes
import os
from PIL import Image, ImageDraw

# Global exit flag
exit_flag = threading.Event()

def listen_for_exit():
    keyboard.wait("Ctrl+Alt")
    exit_flag.set()

def set_cursor(path):
    cursor_path = os.path.abspath(path)
    ctypes.windll.user32.SetSystemCursor(ctypes.windll.user32.LoadImageW(
        0, cursor_path, 2, 0, 0, 0x00000010), 32512)  # 32512 = OCR_NORMAL

def restore_default_cursor():
    ctypes.windll.user32.SystemParametersInfoW(87, 0, None, 0)  # SPI_SETCURSORS = 87

# Create a big gradient blue circle cursor (now 256x256)
def create_big_blue_circle_cursor(path="big_blue_circle_cursor.cur"):
    size = (562, 562)  # Bigger cursor size 256x256
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    # Draw a big circle in the center
    circle_center = (size[0] // 2, size[1] // 2)
    radius = size[0] // 2 - 16  # Leave a small margin for the larger size

    for r in range(radius, 0, -1):
        t = r / radius
        # Gradient from deep blue (outside) to light blue (inside)
        outer_blue = np.array([0, 0, 128])   # Darker blue
        inner_blue = np.array([173, 216, 230])  # Lighter blue (sky blue)
        color = tuple((1-t) * inner_blue + t * outer_blue)
        color = tuple(map(int, color)) + (255,)  # Add full alpha

        bbox = [
            circle_center[0] - r, circle_center[1] - r,
            circle_center[0] + r, circle_center[1] + r
        ]
        draw.ellipse(bbox, outline=color)

    # Save as .ico then rename to .cur
    image.save("big_blue_circle_cursor.ico")
    if os.path.exists(path):
        os.remove(path)
    os.rename("big_blue_circle_cursor.ico", path)

# Gesture recognition and mouse control
def gestr_recog():
    pyautogui.FAILSAFE = False
    threading.Thread(target=listen_for_exit, daemon=True).start()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    screen_width, screen_height = pyautogui.size()
    cap = cv2.VideoCapture(0)

    clicking = False
    smoothing_factor = 5
    mouse_positions = []
    hand_cursor_applied = False
    no_hand_counter = 0

    while cap.isOpened() and not exit_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        hand_detected = False

        if result.multi_hand_landmarks:
            hand_detected = True
            no_hand_counter = 0  # reset no-hand counter

            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger = hand_landmarks.landmark[8]
                middle_finger = hand_landmarks.landmark[12]
                ring_finger = hand_landmarks.landmark[16]
                pinky_finger = hand_landmarks.landmark[20]
                thumb = hand_landmarks.landmark[4]

                if (index_finger.y < middle_finger.y and
                    index_finger.y < ring_finger.y and
                    index_finger.y < pinky_finger.y and
                    thumb.y > index_finger.y):

                    screen_x = int(index_finger.x * screen_width * 2)
                    screen_y = int(index_finger.y * screen_height * 2)
                    mouse_positions.append((screen_x, screen_y))
                    if len(mouse_positions) > smoothing_factor:
                        mouse_positions.pop(0)
                    smoothed_x = int(np.mean([pos[0] for pos in mouse_positions]))
                    smoothed_y = int(np.mean([pos[1] for pos in mouse_positions]))
                    pyautogui.moveTo(smoothed_x, smoothed_y)

                distance = abs(index_finger.x - thumb.x) + abs(index_finger.y - thumb.y)
                if distance < 0.05:
                    if not clicking:
                        pyautogui.click()
                        clicking = True
                else:
                    clicking = False

        else:
            no_hand_counter += 1

        # Handle cursor swap
        if hand_detected and not hand_cursor_applied:
            set_cursor("big_blue_circle_cursor.cur")
            hand_cursor_applied = True
        elif not hand_detected and hand_cursor_applied and no_hand_counter > 10:
            restore_default_cursor()
            hand_cursor_applied = False

        cv2.imshow('Gesture Mouse Control', frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
    restore_default_cursor()

def gestrecog():
    try:
        # Create the custom larger cursor
        create_big_blue_circle_cursor("big_blue_circle_cursor.cur")
        gestr_recog()
    finally:
        restore_default_cursor()  # Make sure cursor is restored even if something breaks

if __name__ == "__main__":
    gestrecog()