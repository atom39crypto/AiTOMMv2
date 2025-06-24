import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import re

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    raise ImportError("Please install tkinterdnd2 using 'pip install tkinterdnd2'")

def create_text_input_ui(hotkey_text):
    ui = TkinterDnD.Tk()
    ui.overrideredirect(True)
    ui.attributes("-topmost", True)
    ui.configure(bg='white')
    ui.attributes("-alpha", 0.8)
    base_height = 130
    ui.geometry(f"450x{base_height}+1470+30")

    border_frame = tk.Frame(ui, bg="#4169E1", bd=2)
    border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    fig = Figure(figsize=(9, 3), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    x = np.linspace(0, 2, 1000)
    num_waves = 5
    lines = [ax.plot(x, np.sin(2 * np.pi * x), linewidth=3)[0] for _ in range(num_waves)]
    ax.set_xlim(0, 2)
    ax.set_ylim(-1, 1)
    ax.set_facecolor("#FFFFFF")
    ax.grid(color="#4169E1", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.axis('off')

    canvas = FigureCanvasTkAgg(fig, master=border_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def animate(i, lines, x):
        colors = ["#8A2BE2", "#6A5ACD", "#4169E1", "#1E90FF", "#00BFFF"]
        for j, line in enumerate(lines):
            phase_shift = j * 0.2
            amplitude = 0.4 - (j * 0.05)
            y = -0.4 + amplitude * np.sin(2 * np.pi * (x - 0.01 * i) + phase_shift)
            line.set_ydata(y)
            line.set_color(colors[j % len(colors)])
            line.set_alpha(1)
        return lines

    ani = animation.FuncAnimation(fig, animate, fargs=(lines, x), frames=200, interval=10, blit=True)

    input_frame = tk.Frame(border_frame, bg="white")
    input_frame.place(relx=0.5, y=2, anchor="n")

    text_box = tk.Text(input_frame, font=("Helvetica", 14), width=30, height=1, bd=2, relief="groove", wrap="word")
    text_box.pack(side="left", padx=5, pady=5)

    # Track dropped files: {placeholder_label: real_path}
    dropped_files = {}

    def on_key(event):
        if event.keysym == "Return" and not (event.state & 0x0001):  # Shift not held
            submit_text()
            return "break"
        update_height()

    def update_height():
        line_count = int(text_box.index('end-1c').split('.')[0])
        text_box.configure(height=line_count)
        new_height = base_height + (line_count - 1) * 25
        ui.geometry(f"450x{new_height}+1470+30")

    def submit_text():
        user_input = text_box.get("1.0", "end-1c")

        # Replace any 📄 filename occurrences with the real path
        final_text = user_input
        for label, path in dropped_files.items():
            final_text = final_text.replace(label, path)

        if final_text.strip():
            hotkey_text.value = final_text

        ui.destroy()

    text_box.bind("<KeyRelease>", on_key)

    close_button = tk.Button(
        input_frame, text="✖", font=("Helvetica", 22, "bold"), fg="#8A2BE2",
        bg="white", width=2, height=1, border=0, relief="flat",
        padx=1, pady=1, activebackground="#d1c4e9",
        command=ui.destroy
    )
    close_button.pack(side="left", padx=10)

    def handle_drop(event):
        filepath = event.data.strip().strip('{}')
        filename = os.path.basename(filepath)
        placeholder = f"📄 {filename}"

        cursor_pos = text_box.index(tk.INSERT)
        text_box.insert(cursor_pos, placeholder)

        # Map placeholder to actual file path
        dropped_files[placeholder] = filepath
        update_height()

    text_box.drop_target_register(DND_FILES)
    text_box.dnd_bind('<<Drop>>', handle_drop)

    ui.mainloop()
