# Add this at the very top of your code (first import)
import tkinter as tk

# Monkey-patch Image.__del__ to suppress the error
_original_image_del = tk.Image.__del__

def _patched_image_del(self):
    try:
        _original_image_del(self)
    except RuntimeError as e:
        if "main thread is not in main loop" in str(e):
            pass  # Silence this specific error
        else:
            raise

tk.Image.__del__ = _patched_image_del

# Then keep the rest of your original code below
import numpy as np
from matplotlib.figure import Figure
# ... rest of your imports and original code ...
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

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

def create_wave_animation(prompt_text):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg='white')
    root.attributes("-alpha", 0.8)
    root.geometry("450x130+1470+30")

    border_frame = tk.Frame(root, bg="#4169E1", bd=2)
    border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    fig = Figure(figsize=(9, 3), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])

    ax.text(0.5, 0.75, prompt_text, transform=ax.transAxes,
            fontsize=14, color="black", ha='center', va='center', weight='bold')

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

    ani = animation.FuncAnimation(fig, animate, fargs=(lines, x), frames=200, interval=10, blit=True)
    return root