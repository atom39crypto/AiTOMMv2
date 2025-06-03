import pyautogui
from time import sleep
from Core.AI import mainframe
from Tools.Small_Functions import video_controller, volum, closetab,Last_stand_protocol
from Tools.APPS import open_app, close_app,switch_to_chrome
from Tools.launch_imageGen import launch_third_terminal

def services(questions):
    questions_lower = questions.lower()

    response = ''
    condition_met = False

    if questions_lower in ["shut up", "stop", "quiet"]:
        print("Stopping...")
        condition_met = True

    if any(keyword in questions_lower for keyword in ["pause", "unpause"]):
        switch_to_chrome()
        pyautogui.hotkey("space")
        condition_met = True

    if any(keyword in questions_lower for keyword in ["mute", "unmute"]):
        switch_to_chrome()
        pyautogui.hotkey("m")
        condition_met = True

    if "video" in questions_lower and any(keyword in questions_lower for keyword in ["back", "forward"]):
        switch_to_chrome()
        video_controller(questions)
        condition_met = True

    if "volume" in questions_lower and any(keyword in questions_lower for keyword in ["up", "down", "increase", "reduce", "decrease"]):
        volum(questions)
        condition_met = True

    if "tab" in questions_lower and any(keyword in questions_lower for keyword in ["close", "quit"]):
        switch_to_chrome()
        closetab(questions)
        condition_met = True

    if "change" in questions_lower and "tab" in questions_lower:
        switch_to_chrome()
        pyautogui.hotkey("ctrl", "tab")
        condition_met = True

    if "change window" in questions_lower:
        pyautogui.hotkey("alt", "tab")
        condition_met = True

    if any(keyword in questions_lower for keyword in ["quit", "close"]):
        if "now" in questions_lower:
            pyautogui.hotkey("alt", "tab")
            pyautogui.hotkey("alt", "f4")
        else:
            close_app(questions)
        condition_met = True

    if questions_lower == "last stand protocall":
        excluded_title = "Visual Studio Code"
        Last_stand_protocol(excluded_title)
        condition_met = True

    if questions_lower == "Terminate":
        import sys
        sys.exit()
        condition_met = True

    if "image" in questions_lower and any(keyword in questions_lower for keyword in ["alter", "modify","change"]):
        launch_third_terminal(questions)
        condition_met = True

    if not condition_met:
        response = mainframe(questions)

    return response




if __name__ == "__main__":
    #questions = input("enter : ")
    sleep(2)
    questions = "last stand protocall"
    services(questions)