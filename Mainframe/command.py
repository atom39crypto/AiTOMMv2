import threading
import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gc
import os

from Core.AI import mainframe
from Frontend.background.TTS_ui import run_tts_app
from Mainframe.simple_tools import services

root = None
stop_event = threading.Event()
response_ready = threading.Event()
response_holder = []

def animate(i, lines, x):
    colors = ["#8A2BE2", "#6A5ACD", "#4169E1", "#1E90FF", "#00BFFF"]
    for j, line in enumerate(lines):
        phase_shift = j * 0.2
        amplitude = 0.6 - (j * 0.05)  # Increased from 0.4 to 0.6
        y = -0.4 + amplitude * np.sin(2 * np.pi * (x - 0.01 * i) + phase_shift)
        line.set_ydata(y)
        line.set_color(colors[j % len(colors)])
        line.set_alpha(1)
    return lines


def close_program():
    stop_event.set()
    try:
        if root:
            root.after(0, root.destroy)
    except:
        pass
    os._exit(0)

def create_wave_animation(prompt_text):
    global root
    try:
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg='white')
        root.attributes("-alpha", 0.8)

        # Default size
        default_width = 450
        default_height = 130
        root.geometry(f"{default_width}x{default_height}+1470+30")
        root.minsize(default_width, default_height)
        root.maxsize(1000, 400)  # max size limit

        # Outer blue border
        border_frame = tk.Frame(root, bg="#4169E1", bd=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # White inner content
        content_frame = tk.Frame(border_frame, bg="white", padx=12, pady=8)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Prompt + Close
        top_bar = tk.Frame(content_frame, bg="white")
        top_bar.pack(fill=tk.X, side=tk.TOP)

        prompt_label = tk.Label(
            top_bar,
            text=prompt_text,
            font=("Helvetica", 13, "bold"),
            fg="black",
            bg="white",
            wraplength=default_width - 80,  # leave space for close button and padding
            justify="left"
        )
        prompt_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        close_btn = tk.Button(
            top_bar,
            text="✖",
            font=("Helvetica", 18, "bold"),
            fg="#8A2BE2",
            bg="white",
            border=0,
            relief="flat",
            activebackground="#d1c4e9",
            command=close_program,
            padx=4,
            pady=0,
            width=2,
            height=1
        )
        close_btn.pack(side=tk.RIGHT, anchor='n')

        # Measure the needed height for the label's text (wrapped)
        root.update_idletasks()
        needed_height = prompt_label.winfo_reqheight()
        # If text height exceeds approx 60 pixels (1 line ~20, so 3+ lines), increase window height
        if needed_height > 60:
            new_height = default_height + (needed_height - 60)
            root.geometry(f"{default_width}x{new_height}+1470+30")

        # Wave animation
        fig = Figure(figsize=(6, 2.5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_position([0, 0, 1, 1])
        x = np.linspace(0, 2, 1000)
        lines = [ax.plot(x, np.sin(2 * np.pi * x), linewidth=3)[0] for _ in range(5)]
        ax.set_xlim(0, 2)
        ax.set_ylim(-1, 1)
        ax.set_facecolor("#FFFFFF")
        ax.grid(color="#4169E1", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas_widget = canvas.get_tk_widget()
        # Fixed spacing ~20px vertical padding between text and wave
        canvas_widget.pack(fill=tk.BOTH, expand=True, pady=(4, 4))

        ani = animation.FuncAnimation(fig, animate, fargs=(lines, x), frames=200, interval=10, blit=True)

        root.mainloop()

    except Exception as e:
        print(f"[UI Error] {e}")
    finally:
        try:
            if root:
                root.quit()
                root.destroy()
        except Exception as cleanup_error:
            print(f"[Cleanup Error] {cleanup_error}")
        tk._default_root = None
        gc.collect()

def run_mainframe(prompt):
    if prompt.lower() in ["shut up", "stop", "quiet"]:
        print("Stopping...")
        close_program()
        return
    if stop_event.is_set():
        return
    response = services(prompt)
    if not stop_event.is_set():
        response_holder.append(response)
        response_ready.set()
        try:
            if root:
                root.after(0, root.destroy)
        except:
            pass

def allCommands(prompt="Hello world"):
    global root

    animation_thread = threading.Thread(target=create_wave_animation, args=(prompt,))
    mainframe_thread = threading.Thread(target=run_mainframe, args=(prompt,))

    animation_thread.start()
    mainframe_thread.start()

    response_ready.wait(timeout=10)

    mainframe_thread.join()
    animation_thread.join()

    if not stop_event.is_set() and response_holder:
        run_tts_app(response_holder[0])
    else:
        print("TTS skipped (user canceled or no response).")

if __name__ == "__main__":
    allCommands("This is a longer prompt that wraps correctly and fits inside the UI without overflowing or hiding the button.")
