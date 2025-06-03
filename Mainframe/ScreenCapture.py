import tkinter as tk
from PIL import ImageGrab
import pyperclip
import os

def capture_screenshot():
    def on_mouse_down(event):
        nonlocal start_x, start_y
        start_x = root.winfo_pointerx()
        start_y = root.winfo_pointery()
        canvas.delete("selection")

    def on_mouse_drag(event):
        end_x = root.winfo_pointerx()
        end_y = root.winfo_pointery()
        canvas.delete("selection")
        canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='red', width=2, tag="selection")

    def on_mouse_up(event):
        root.withdraw()
        end_x = root.winfo_pointerx()
        end_y = root.winfo_pointery()

        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        os.makedirs("screenshots", exist_ok=True)
        file_path = os.path.abspath(f"screenshots/screenshot.png")
        img.save(file_path)
        pyperclip.copy(file_path)
        print(f"Screenshot saved and path copied: {file_path}")
        root.destroy()
        # Send back the path
        screenshot_path.append(file_path)

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(bg='black')
    root.attributes("-topmost", True)

    canvas = tk.Canvas(root, bg="gray", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    start_x = start_y = 0
    screenshot_path = []

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    
    return screenshot_path[0] if screenshot_path else None

