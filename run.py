import multiprocessing
import threading
import keyboard
import tkinter as tk
from tkinter import ttk
import time
import pyperclip

from Mainframe.ScreenCapture import capture_screenshot
from Audio.HWD import hot_word_detection
from Mainframe.command import allCommands
from Frontend.background.run_ui import create_text_input_ui
from main import StartUI

ui_process = None  # Global reference to track UI process


def show_splash_and_initialize(init_func, width=400, height=200):
    splash = tk.Tk()
    splash.title("Loading...")
    splash.geometry(f"{width}x{height}")
    splash.resizable(False, False)

    splash.update_idletasks()
    ws = splash.winfo_screenwidth()
    hs = splash.winfo_screenheight()
    x = (ws // 2) - (width // 2)
    y = (hs // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")

    label = ttk.Label(splash, text="Initializing, please wait...", font=(None, 14))
    label.pack(pady=20)
    progress = ttk.Progressbar(splash, mode='indeterminate', length=300)
    progress.pack(pady=10)
    progress.start(10)

    def run_init():
        try:
            init_func()
        finally:
            splash.quit()

    threading.Thread(target=run_init, daemon=True).start()
    splash.mainloop()
    splash.destroy()


def HWD_wrapper(queue):
    while True:
        text = hot_word_detection()
        if text:
            queue.put(text)


def f8_listener(hotkey_text):
    global ui_process
    while True:
        keyboard.wait('F8')
        time.sleep(0.2)  # debounce
        if ui_process is None or not ui_process.is_alive():
            print("Launching Eel UI...")
            ui_process = multiprocessing.Process(target=StartUI)
            ui_process.start()
        else:
            print("UI is already running.")


def launch_f8_listener(hotkey_text):
    listener = threading.Thread(target=f8_listener, args=(hotkey_text,), daemon=True, name="F8ListenerThread")
    listener.start()


def ui_thread_launcher(hotkey_text, manual_input_open_flag):
    create_text_input_ui(hotkey_text)
    manual_input_open_flag.value = False


def process_text_input(input_text):
    if input_text:
        print(f"Processing text input: {input_text}")
        p = multiprocessing.Process(target=allCommands, args=(input_text,))
        p.start()
        p.join()


def trigger_input_input(hotkey_text):
    if hotkey_text.value:
        process_text_input(hotkey_text.value)
        hotkey_text.value = ""


def initialize_system():
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    hotkey_text = manager.Value("s", "")
    manual_input_open = manager.Value("b", False)
    queue = multiprocessing.Queue()

    hwd = multiprocessing.Process(target=HWD_wrapper, args=(queue,))
    hwd.daemon = True
    hwd.start()

    launch_f8_listener(hotkey_text)

    print("Press 'F8' to activate the chatbot...")
    print("System is listening for commands ...\n")

    return {"hotkey_text": hotkey_text, "manual_input_open": manual_input_open, "queue": queue}


if __name__ == "__main__":
    def do_init():
        global startup
        startup = initialize_system()

    show_splash_and_initialize(do_init)

    hotkey_text = startup["hotkey_text"]
    manual_input_open = startup["manual_input_open"]
    queue = startup["queue"]

    while True:
        cmd = None
        if hotkey_text.value:
            cmd = hotkey_text.value
            hotkey_text.value = ""
        elif not queue.empty():
            cmd = queue.get()

        if (not manual_input_open.value and
            keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('alt')):
            manual_input_open.value = True
            print("Shortcut detected! Opening text input UI...")
            threading.Thread(
                target=ui_thread_launcher,
                args=(hotkey_text, manual_input_open),
                daemon=True
            ).start()

        if keyboard.is_pressed('shift') and keyboard.is_pressed('ctrl') and keyboard.is_pressed('space'):
            print("Capturing screenshot...")
            path = capture_screenshot()
            if path:
                print(f"Feeding screenshot path to allCommands: {path}")
                p = multiprocessing.Process(target=allCommands, args=(path,))
                p.start()
                p.join()
            time.sleep(1)

        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift') and keyboard.is_pressed('c'):
            print("Capturing screenshot (clipboard only)...")
            path = capture_screenshot()
            if path:
                pyperclip.copy(path)
                print(f"Screenshot saved and path copied to clipboard: {path}")
            time.sleep(1)

        if cmd:
            print(f"Command detected: {cmd}")
            p = multiprocessing.Process(target=allCommands, args=(cmd,))
            p.start()
            p.join()

        trigger_input_input(hotkey_text)
        time.sleep(0.1)
