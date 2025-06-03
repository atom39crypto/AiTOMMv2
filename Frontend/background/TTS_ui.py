import tkinter as tk
import threading
from Audio.TTS import TTS

class TTSApp:
    def __init__(self, root, text):
        self.root = root
        self.root.overrideredirect(True)  
        self.root.attributes("-topmost", True)
        self.root.configure(bg='white')
        self.root.attributes("-alpha", 0.8)  
        self.root.geometry("450x130+1470+30")  

        border_frame = tk.Frame(root, bg="#4169E1", bd=2)  
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        content_frame = tk.Frame(border_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True)

        self.output_label = tk.Label(content_frame, text="", font=("Arial", 12), bg="white", fg="black", wraplength=420)
        self.output_label.pack(pady=20)

        self.text = text
        self.speak()

    def speak(self):
        threading.Thread(target=self.start_speaking, daemon=True).start()

    def start_speaking(self):
        tts_player = TTS(self.text, language='bn')
        tts_player.ui_callback = self.update_text
        tts_player.ui_close_callback = self.close_ui  
        tts_player.play_all()

    def update_text(self, chunk_text):
        self.output_label.config(text=chunk_text)

    def close_ui(self):
        print("Closing UI as speaking is over...")
        self.root.quit()  

def run_tts_app(text):
    root = tk.Tk()
    app = TTSApp(root, text)
    root.mainloop()

if __name__ == "__main__":
    text = """Greetings,I it seems that This is our first time interacting with each other.Can you please tell me your name ?"""
    run_tts_app(text)
