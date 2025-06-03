import eel
import keyboard  # Requires the `keyboard` library to detect key presses
from Core.AI import mainframe

eel.init("Frontend/Chatbot_Tutorial 0.5")  # The "web" folder should contain your index.html, script.js, and style.css

@eel.expose
def get_response(user_message):
    
    response = mainframe(user_message)
    print(f"User: {user_message} -> Bot: {response}")  # Debug log
    return response

def StartUI():
    print("Starting chatbot...")
    eel.start("index.html", size=(600, 600))

if __name__ == "__main__":
    StartUI()