import re
import pyautogui
from time import sleep
from word2number import w2n
import win32gui
import win32con
import pywhatkit as kit
import webbrowser

from Tools.APPS import switch_to_chrome


import ctypes
from time import sleep

def catch_site(questions):
    websites = c.website
    website = websites.keys()
    for word in questions.split():
        if word in website:
            return word


def find_domains(text):
    # Regular expression pattern for matching domain names
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    
    # Find all matches in the text
    domains = re.findall(domain_pattern, text)
    
    return domains

def extract_integer(text):
    digit_match = re.search(r'\d+', text)
    if digit_match:
        return int(digit_match.group())
    try:
        return w2n.word_to_num(text)
    except Exception as e:
        print("Could not extract an integer:", e)
        return None

def webpage(a):
    print(f'<=--------------------Webpage {a}----------------------=>')
    if a:
        webbrowser.open(a)
    else:
        search(a)
    return a

def video_controller(a, b=0):
    b = extract_integer(a)
    direction = 'right' if 'forward' in a.lower() else 'left' if any(k in a.lower() for k in ["back", "rewind"]) else None
    pyautogui.hotkey("alt", "tab")
    for _ in range(0, b, 5):
        pyautogui.press(direction)
        sleep(0.5)
    return a

def volum(a):
    n = extract_integer(a)
    VK_VOLUME_UP, VK_VOLUME_DOWN = 0xAF, 0xAE

    def press_key(key_code):
        ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

    action = VK_VOLUME_UP if any(k in a.lower() for k in ["up", "increase"]) else VK_VOLUME_DOWN if any(k in a.lower() for k in ["down", "reduce", "decrease"]) else None
    for _ in range(0, n, 2):
        press_key(action)
        sleep(0.3)
    return a

def closetab(a):
    a = extract_integer(a)
    i = 0
    switch_to_chrome()
    while(i<a):
        pyautogui.hotkey("ctrl","w")
        sleep(1)
        i=i+1
    return str(a)



def search(a):
    kit.search(a)
    return a   

def Last_stand_protocol(excluded_title):
    def callback(hwnd, extra):
        print(f"Window Handle: {hwnd}")
        window_text = win32gui.GetWindowText(hwnd).strip()

        # Check if window should be excluded or if it's empty
        if excluded_title.lower() not in window_text.lower() and window_text:
            print(f"Closing window: '{window_text}'")

            if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
                try:
                    # Restore window if minimized before closing
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    # Send a close message to the window
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                except win32gui.error as e:
                    print(f"Error closing window '{window_text}': {e}")
            else:
                print(f"Invalid or hidden window handle: '{window_text}'")
        else:
            print(f"Keeping window open: '{window_text}'")

    # Enumerate all windows and apply the callback
    win32gui.EnumWindows(callback, None)
    sleep(10)
    pyautogui.press('enter')

if __name__ == "__main__":
    excluded_title = "Visual Studio Code"
    Last_stand_protocol(excluded_title)

