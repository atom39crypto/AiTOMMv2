import pyautogui
import pywhatkit as kit
from pynput.keyboard import Key, Controller
from time import sleep
# from engine.Weilder.services.APPS import switch_to_chrome


def youtube(a):
    print("<-------------------------------youtube------------------------->")
    try:
        kit.playonyt(a)
        return f"Playing video: {a}"
    except Exception as e:
        return f"Error playing video: {str(e)}"
    
def video_controller(a,b):
    keyboard = Controller()
    i = 0
    print("<------------------------------ working --------------------------->")
    questions = a
    # switch_to_chrome()
    if "pause" in questions.lower() or "unpause" in questions.lower():
        pyautogui.hotkey("k")

    if "mute" in questions.lower() or "unmute" in questions.lower():
        pyautogui.hotkey("m")

    if "forward" in questions.lower():
        print("passing")
        
        
        while i < b:
            pyautogui.press('right')
            sleep(0.5)
            i += 5
    
    if "back" in questions.lower():
        print("passing")
        


        while i < b:
            pyautogui.press('left')
            sleep(0.5)
            i += 5
    return a