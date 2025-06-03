import os
import ctypes
import cv2
import dlib
import pyautogui
import numpy as np
import time
import threading
import keyboard
from PIL import Image, ImageDraw

# Global exit flag
enable_exit = threading.Event()

# Cursor utilities
def set_cursor(path):
    cursor_path = os.path.abspath(path)
    ctypes.windll.user32.SetSystemCursor(
        ctypes.windll.user32.LoadImageW(
            0, cursor_path, 2, 0, 0, 0x00000010
        ),
        32512  # OCR_NORMAL
    )


def restore_default_cursor():
    ctypes.windll.user32.SystemParametersInfoW(87, 0, None, 0)  # SPI_SETCURSORS

# Create an eye-shaped cursor with white sclera, purple-to-blue iris gradient, and black pupil
# Saves as .cur file at given path
def create_eye_cursor(path="eye_cursor.cur"):
    # Cursor image size
    size = (562, 562)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    center = (size[0] // 2, size[1] // 2)
    # Eyeball (sclera)
    sclera_bbox = [center[0] - 250, center[1] - 150, center[0] + 250, center[1] + 150]
    draw.ellipse(sclera_bbox, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4)

    # Iris gradient
    iris_radius = 80
    for r in range(iris_radius, 0, -1):
        t = r / iris_radius
        # gradient from purple at edge to blue at center
        outer = np.array([128, 0, 128])  # Purple
        inner = np.array([0, 0, 255])    # Blue
        color = tuple((1 - t) * inner + t * outer)
        color = tuple(map(int, color)) + (255,)
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        draw.ellipse(bbox, outline=color)

    # Pupil
    pupil_radius = 30
    pupil_bbox = [center[0] - pupil_radius, center[1] - pupil_radius,
                  center[0] + pupil_radius, center[1] + pupil_radius]
    draw.ellipse(pupil_bbox, fill=(0, 0, 0, 255))

    # Save and convert to cursor
    ico_path = os.path.splitext(path)[0] + ".ico"
    image.save(ico_path)
    if os.path.exists(path):
        os.remove(path)
    os.rename(ico_path, path)

# Listen for 'q' to exit
def listen_for_exit():
    keyboard.wait('Ctrl+Alt')
    enable_exit.set()

# Main eye-tracking and cursor control
def run_eye_tracker():
    # Prepare and set custom cursor
    cursor_file = 'eye_cursor.cur'
    create_eye_cursor(cursor_file)
    set_cursor(cursor_file)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        r"VisualIntelligence\Gesture_recognition\shape_predictor_68_face_landmarks.dat"
    )
    cap = cv2.VideoCapture(0)

    screen_w, screen_h = pyautogui.size()
    pyautogui.FAILSAFE = False

    def midpoint(p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    smoothing = 0.5
    last_x, last_y = screen_w / 2, screen_h / 2

    click_threshold = 0.05
    click_wait_time = 2
    last_click_time = time.time()
    fixed_x, fixed_y = None, None

    def get_screen_elements():
        return [(100, 100), (200, 200), (500, 500)]

    def apply_gravity(x, y, elements, gravity_strength=50):
        for ex, ey in elements:
            dist = np.hypot(x - ex, y - ey)
            if dist < gravity_strength:
                pull = (gravity_strength - dist) / gravity_strength
                x += (ex - x) * pull * 0.1
                y += (ey - y) * pull * 0.1
        return x, y

    def check_and_click(x, y):
        nonlocal fixed_x, fixed_y, last_click_time
        now = time.time()
        if fixed_x is None:
            fixed_x, fixed_y = x, y
            last_click_time = now
        elif (abs(fixed_x - x) < click_threshold * screen_w and
              abs(fixed_y - y) < click_threshold * screen_h):
            if now - last_click_time > click_wait_time:
                pyautogui.click(x, y)
                last_click_time = now
                fixed_x, fixed_y = None, None
        else:
            fixed_x, fixed_y = x, y
            last_click_time = now

    # Start exit listener thread
    threading.Thread(target=listen_for_exit, daemon=True).start()

    while not enable_exit.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            lm = predictor(gray, face)
            l = midpoint(lm.part(36), lm.part(39))
            r = midpoint(lm.part(42), lm.part(45))
            ex = (l[0] + r[0]) / 2
            ey = (l[1] + r[1]) / 2

            sx = np.interp(ex, [250, 540], [0, screen_w * 2.2])
            sy = np.interp(ey, [220, 380], [0, screen_h * 2.5])

            cx = last_x + (sx - last_x) * smoothing
            cy = last_y + (sy - last_y) * smoothing

            cx, cy = apply_gravity(cx, cy, get_screen_elements())

            # Clamp to screen bounds
            cx = max(0, min(cx, screen_w - 1))
            cy = max(0, min(cy, screen_h - 1))

            pyautogui.moveTo(cx, cy)
            check_and_click(cx, cy)

            last_x, last_y = cx, cy
            cv2.circle(frame, l, 3, (0, 255, 0), -1)
            cv2.circle(frame, r, 3, (0, 255, 0), -1)

        # cv2.imshow("Eye Tracking", frame)

    cap.release()
    cv2.destroyAllWindows()
    restore_default_cursor()

if __name__ == "__main__":
    run_eye_tracker()
