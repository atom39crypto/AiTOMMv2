import os
import pyautogui
import pygetwindow as gw
import win32gui
import pywintypes
import ctypes
import time
from time import sleep
from pywinauto import application, findwindows

import Tools.contacts as c


def catch_app(questions):
    apps = c.apps.keys()
    for word in questions.split():
        if word in apps:
            return word
    return None


def allow_foreground_change():
    hwnd = win32gui.GetForegroundWindow()
    ctypes.windll.user32.AllowSetForegroundWindow(ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0))


def switch_to_chrome():
    try:
        chrome_windows = findwindows.find_windows(title_re=".*Chrome.*")
        if chrome_windows:
            app = application.Application().connect(handle=chrome_windows[0])
            window = app.window(handle=chrome_windows[0])
            window.set_focus()
            print(f"Switched to: {window.window_text()}")
        else:
            os.system("start chrome.exe")
    except Exception as e:
        print(f"An error occurred: {e}")


def handle_existing_window(app):
    windows = gw.getWindowsWithTitle(app.capitalize())
    if windows:
        for window in windows:
            hwnd = window._hWnd
            try:
                allow_foreground_change()
                win32gui.ShowWindow(hwnd, 9)  # Restore window
                time.sleep(0.5)
                win32gui.SetForegroundWindow(hwnd)
                print(f"Restored and switched to: '{window.title}' (HWND: {hwnd})")
            except pywintypes.error as e:
                print(f"Error bringing window to foreground: {e}")
                print("Simulating Alt+Tab to switch to the window.")
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)
                win32gui.SetForegroundWindow(hwnd)
            return True
    return False


def start_application(apps, app):
    print(f"No running window found for {app}. Attempting to start {app}.")
    try:
        os.system(f"start {apps[app]}")
        return True
    except Exception as e:
        print(f"Failed to start {app}: {e}")
        return False


def launch_with_search(questions):
    pyautogui.press("super")
    pyautogui.typewrite(questions)
    pyautogui.press("enter")


def open_app(questions):
    print(f"<----------------------------------{questions}------------------------------>")
    try:
        if "chromeApps" in questions:
            switch_to_chrome()
            return questions

        apps = c.apps
        for app in apps.keys():
            if app.lower() in questions.lower():
                print(f"Looking for windows with the title containing: {app}")
                if handle_existing_window(app) or start_application(apps, app):
                    return questions

        launch_with_search(questions)
        return "Application Launched"
    except Exception as e:
        print(f"An error occurred: {e}")
        launch_with_search(questions)
        return "Application Launched"


def close_app(questions):
    apps = c.apps
    print("Quitting ..........")
    for app, exe in apps.items():
        if app in questions:
            os.system(f"c:\\windows\\system32\\taskkill.exe /f /im {exe}.exe")
    return "Quitting .........."


if __name__ == "__main__":
    sleep(2)
    questions = "discord"
    open_app(questions)
