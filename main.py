import eel
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from Core.AI import mainframe
import base64
import os

eel.init("Frontend/Chatbot_Tutorial 0.5")

@eel.expose
def save_file(file_name, data_url):
    import base64
    import os

    folder = r"E:\python\AI\ATOM\Atom - 8.2\screenshots"
    os.makedirs(folder, exist_ok=True)

    header, encoded = data_url.split(",", 1)
    file_path = os.path.join(folder, file_name)

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(encoded))

    print(f"Saved file: {file_path}")



@eel.expose
def get_response(user_message):
    response = mainframe(user_message)
    print(f"User: {user_message} -> Bot: {response}")
    return response

@eel.expose
def select_file():
    try:
        root = Tk()
        root.withdraw()
        file_path = askopenfilename()
        root.destroy()
        print(f"Selected file: {file_path}")
        return file_path or ""  # Return empty string if cancelled
    except Exception as e:
        print(f"Error opening file dialog: {e}")
        return ""
    
def StartUI():
    print("Starting chatbot...")
    eel.start("index.html", size=(1200, 1200))

if __name__ == "__main__":
    StartUI()
