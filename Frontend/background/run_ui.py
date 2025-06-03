import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    # For drag-and-drop support
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    raise ImportError("Please install tkinterdnd2 using 'pip install tkinterdnd2'")

def create_text_input_ui(hotkey_text):
    """
    Creates a Tkinter window with an animated wave background and a text input area.
    Supports drag-and-drop file paths into the input box.
    When submitted, stores the input text into the hotkey_text.value.
    """
    ui = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop
    ui.overrideredirect(True)
    ui.attributes("-topmost", True)
    ui.configure(bg='white')
    ui.attributes("-alpha", 0.8)
    ui.geometry("450x130+1470+30")

    # Frame with Royal Blue border
    border_frame = tk.Frame(ui, bg="#4169E1", bd=2)
    border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    # Animated background
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

    # Input frame
    input_frame = tk.Frame(border_frame, bg="white")
    input_frame.place(relx=0.5, rely=0.24, anchor="center")
    entry = tk.Entry(input_frame, font=("Helvetica", 14), width=30, bd=2, relief="groove")
    entry.pack(side="left", padx=5, pady=5)

    def submit_text(event=None):
        user_input = entry.get().strip()
        if user_input:
            hotkey_text.value = user_input
        ui.destroy()

    # Close button
    close_button = tk.Button(
        input_frame, text="✖", font=("Helvetica", 22, "bold"), fg="#8A2BE2",
        bg="white", width=2, height=1, border=0, relief="flat",
        padx=1, pady=1, activebackground="#d1c4e9",
        command=ui.destroy
    )
    close_button.pack(side="left", padx=10)

    entry.bind("<Return>", submit_text)

    # Drag-and-drop file support
    def handle_drop(event):
        filepath = event.data.strip().strip('{}')  # Clean up filepath
        entry.delete(0, tk.END)
        entry.insert(0, filepath)

    entry.drop_target_register(DND_FILES)
    entry.dnd_bind('<<Drop>>', handle_drop)

    ui.mainloop()

