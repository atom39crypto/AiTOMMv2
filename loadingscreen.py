import tkinter as tk
from PIL import Image, ImageTk
import time

def display_loading_screen(image_path):
    root = tk.Tk()
    root.title("Loading...")

    root.overrideredirect(True)

    image = Image.open(image_path)

    width, height = image.size
    image = image.resize((width // 2, height // 2))

    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.pack()

    window_width = image.width
    window_height = image.height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = (screen_height // 2) - (window_height // 2)
    position_right = (screen_width // 2) - (window_width // 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    root.update()

    time.sleep(5)

    root.destroy()
