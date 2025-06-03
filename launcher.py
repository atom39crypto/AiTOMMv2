import subprocess
import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import signal
import pyautogui
import time

# Globals for process handles
proc1 = None
proc2 = None
proc3 = None

def launch_scripts():
    global proc1, proc2, proc3
    activate_path = os.path.join("AiTOMM", "Scripts", "activate.bat")

    # Launching the first script without showing the terminal
    proc1 = subprocess.Popen(
        ["cmd.exe", "/c", f"{activate_path} && python run.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # Launching the second script without showing the terminal
    proc2 = subprocess.Popen(
        ["cmd.exe", "/c", f"{activate_path} && python VisualIntelligence\\VisualInteligence.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    # Launching the third script without showing the terminal
    proc3 = subprocess.Popen(
        ["cmd.exe", "/c", f"{activate_path} && python python_server.py"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

def quit_app(icon, item):
    global proc1, proc2, proc3
    # Simulate pressing Ctrl + Alt + M
    pyautogui.hotkey('ctrl', 'alt', 'm')

    # Wait for 1 second
    time.sleep(1)

    # Simulate pressing Escape
    pyautogui.press('esc')

    # Stop processes after simulated keypresses
    for proc in [proc1, proc2, proc3]:
        if proc and proc.poll() is None:
            try:
                os.kill(proc.pid, signal.CTRL_BREAK_EVENT)
            except Exception as e:
                print(f"Error killing process {proc.pid}: {e}")
    
    icon.stop()

def create_tray():
    image = Image.open("Icon.png")
    icon = pystray.Icon("TrayRunner", image, "Scripts Running", menu=(item("Quit", quit_app),))
    launch_scripts()
    icon.run()

if __name__ == "__main__":
    create_tray()
