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

        # Default window size
        self.default_width = 450
        self.default_height = 130
        self.root.geometry(f"{self.default_width}x{self.default_height}+1470+30")
        self.root.minsize(self.default_width, self.default_height)
        self.root.maxsize(1000, 400)  # Optional: prevent overgrowth

        border_frame = tk.Frame(root, bg="#4169E1", bd=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        content_frame = tk.Frame(border_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True)

        self.output_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 12),
            bg="white",
            fg="black",
            wraplength=self.default_width - 30,
            justify="left"
        )
        self.output_label.pack(pady=(10, 8))

        self.text = text
        self.text_widget = None  # Will be created when needed
        self.content_frame = content_frame  # Save reference
        self.speak()

    def speak(self):
        threading.Thread(target=self.start_speaking, daemon=True).start()

    def start_speaking(self):
        tts_player = TTS(self.text, language='bn')
        tts_player.ui_callback = self.update_text
        tts_player.ui_close_callback = self.close_ui
        tts_player.play_all()

    def update_text(self, chunk_text):
        # Replace label with text widget if not already done
        if self.text_widget is None:
            self.output_label.destroy()
            self.text_widget = tk.Text(
                self.content_frame,
                font=("Arial", 12),
                bg="white",
                fg="black",
                wrap="word",
                height=6,
                bd=0,
                padx=10,
                pady=10
            )
            self.text_widget.pack(pady=(10, 8), fill=tk.BOTH, expand=True)
            self.text_widget.tag_configure("bold", font=("Arial", 12, "bold"))
            self.text_widget.tag_configure("italic", font=("Arial", 12, "italic"))
            self.text_widget.configure(state="disabled")

        def insert_with_format(text):
            idx = 0
            while idx < len(text):
                if text[idx:idx+2] == "**":
                    end = text.find("**", idx+2)
                    if end != -1:
                        self.text_widget.insert("end", text[idx+2:end], "bold")
                        idx = end + 2
                        continue
                elif text[idx] == "*":
                    end = text.find("*", idx+1)
                    if end != -1:
                        self.text_widget.insert("end", text[idx+1:end], "italic")
                        idx = end + 1
                        continue
                self.text_widget.insert("end", text[idx])
                idx += 1

        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        insert_with_format(chunk_text)
        self.text_widget.configure(state="disabled")

        self.root.update_idletasks()
        needed_height = self.text_widget.winfo_reqheight()
        if needed_height > 60:
            new_height = self.default_height + (needed_height - 60)
            self.root.geometry(f"{self.default_width}x{new_height}+1470+30")

    def close_ui(self):
        print("Closing UI as speaking is over...")
        self.root.quit()

def run_tts_app(text):
    root = tk.Tk()
    app = TTSApp(root, text)
    root.mainloop()

if __name__ == "__main__":
    text = (
        "Perform a longJump **NOW** ! Then Drink water and *eat food*. "
        "But not too much.\nThen go to the gym and do some *exercise*. "
        "After that, take a rest and relax.\nRepeat: **NOW** !"
    )
    run_tts_app(text)
