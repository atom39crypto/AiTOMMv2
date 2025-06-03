import socket
import threading
from flask import Flask, Response
import pyautogui
import io
import time
import keyboard

from run import process_text_input
from Tools.Small_Functions import video_controller, volum, closetab, webpage
from Tools.APPS import open_app, close_app, switch_to_chrome
from Tools.launch_imageGen import launch_third_terminal
from converter import transcribe_audio

# === ALT+TAB switcher logic ===
class AltTabSwitcher:
    def __init__(self):
        self.alt_held = False

    def switch_next(self):
        # Ensure Alt is held down
        if not self.alt_held or not keyboard.is_pressed('alt'):
            keyboard.press('alt')
            self.alt_held = True
            print("[Switcher] Alt pressed")

        # Send Tab to cycle
        keyboard.press_and_release('tab')
        print("[Switcher] Tab pressed")

        return "Window cycled"

    def confirm_selection(self):
        if self.alt_held or keyboard.is_pressed('alt'):
            keyboard.press_and_release('enter')
            time.sleep(0.1)
            keyboard.release('alt')
            self.alt_held = False
            print("[Switcher] Enter pressed, Alt released")
            return "Window selected"
        return "No active switch"


# Instantiate the switcher
switcher = AltTabSwitcher()

app = Flask(__name__)

def generate_frames():
    while True:
        screenshot = pyautogui.screenshot().resize((480, 270))
        buffer = io.BytesIO()
        screenshot.save(buffer, format='JPEG')
        frame = buffer.getvalue()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_socket_server():
    host = '0.0.0.0'
    port = 5050

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[Socket] Listening on port {port}...", flush=True)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Socket] Connected by {addr}", flush=True)

        def handle_client(sock):
            try:
                sock.settimeout(5.0)
                initial = sock.recv(1024)

                if not initial:
                    return

                try:
                    decoded = initial.decode().strip()
                    print(f"[Socket] Received: {decoded}", flush=True)

                    # AUDIO HANDLING
                    if decoded == "AUDIO_FILE":
                        print("[Socket] Receiving audio file...", flush=True)
                        audio_path = "received_audio.m4a"
                        with open(audio_path, "wb") as f:
                            while True:
                                try:
                                    chunk = sock.recv(2048)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                                except socket.timeout:
                                    break
                        print(f"[Socket] Audio saved to {audio_path}", flush=True)
                        sock.send(b"AUDIO_RECEIVED")

                        try:
                            transcript = transcribe_audio(audio_path)
                            print(f"[Socket] Transcribed Text: {transcript}", flush=True)
                            process_text_input(transcript)
                        except Exception as e:
                            print(f"[Error in audio processing] {e}", flush=True)
                        return

                    # APP CONTROL
                    if 'App' in decoded:
                        app_name = decoded.split('App ')[1].strip().lower()
                        open_app(app_name)
                        response = f"{app_name} opened!"

                    # WEB
                    elif 'Web' in decoded:
                        web_name = decoded.split('Web ')[1].strip().lower()
                        urls = {
                            "youtube": "https://www.youtube.com",
                            "facebook": "https://www.facebook.com",
                            "instagram": "https://www.instagram.com",
                            "linkedin": "https://www.linkedin.com"
                        }
                        if web_name in urls:
                            webpage(urls[web_name])
                            response = f"{web_name} opened"
                        else:
                            response = "Unknown site"

                    # TEXT COMMAND
                    elif decoded.startswith("TEXT:"):
                        input_text = decoded.split("TEXT:")[1]
                        print(f"[Socket] Text input: {input_text}", flush=True)
                        try:
                            process_text_input(input_text)
                            response = f"Text processed: {input_text}"
                        except Exception as e:
                            response = f"Error in processing text: {e}"
                            print(response, flush=True)

                    # VIDEO COMMANDS
                    elif decoded == "PLAY":
                        keyboard.press('c')
                        time.sleep(0.2)
                        keyboard.release('c')
                        response = "Play pressed"

                    elif decoded == "PAUSE":
                        keyboard.press_and_release('p')
                        response = "Pause pressed"

                    elif decoded == "STOP":
                        keyboard.press('esc')
                        time.sleep(2)
                        keyboard.release('esc')
                        response = "Stop pressed"

                    # SEEK CONTROLS
                    elif decoded.startswith("SeekBar Value:"):
                        if decoded == "SeekBar Value: 1":
                            keyboard.press_and_release('ctrl+alt+a')
                        elif decoded == "SeekBar Value: 2":
                            keyboard.press_and_release('ctrl+alt+g')
                        elif decoded == "SeekBar Value: 3":
                            keyboard.press_and_release('ctrl+alt+e')
                        response = f"Seek adjusted: {decoded}"

                    # BUTTON CONTROLS
                    elif decoded.startswith("button"):
                        actions = {
                            "button0": lambda: (pyautogui.hotkey("enter"),pyautogui.hotkey("alt"), "Enter pressed"),
                            "button1": lambda: (switcher.switch_next(), "Window switched"),
                            "button2": lambda: (pyautogui.hotkey("alt", "f4"), "Window closed"),
                            "button3": lambda: (switch_to_chrome(), pyautogui.hotkey("ctrl", "tab"), "Tab changed"),
                            "button4": lambda: (pyautogui.press("playpause"), "Play/Pause"),
                            "button5": lambda: (keyboard.send("volume mute"), "Muted"),
                            "button6": lambda: (volum('volume up 1'), "Volume up"),
                            "button7": lambda: (volum('volume down 1'), "Volume down"),
                            "button8": lambda: (switch_to_chrome(), closetab('1'), "Tab closed"),
                            "button9": lambda: (switcher.confirm_selection(), "Switch finalized"),
                        }
                        if decoded in actions:
                            result = actions[decoded]()
                            response = result[-1]
                        else:
                            response = f"Unknown button: {decoded}"

                    else:
                        response = f"Unknown command: {decoded}"

                    sock.send(response.encode())

                except UnicodeDecodeError:
                    print("[Socket] Non-text data ignored", flush=True)

            except Exception as e:
                print(f"[Socket] Error: {e}", flush=True)
            finally:
                sock.close()

        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    threading.Thread(target=run_socket_server, daemon=True).start()
    app.run(host='0.0.0.0', port=8000)
