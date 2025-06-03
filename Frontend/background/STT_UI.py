import tkinter as tk
import numpy as np
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def animate(i, lines, x):
    """
    Updates wave animation over time.
    """
    colors = ["#8A2BE2", "#6A5ACD", "#4169E1", "#1E90FF", "#00BFFF"]  # Gradient colors

    for j, line in enumerate(lines):
        phase_shift = j * 0.2  # Staggered movement
        amplitude = 0.6 - (j * 0.1)  # Decreasing amplitude for layered effect
        y = amplitude * np.sin(2 * np.pi * (x - 0.01 * i) + phase_shift)
        line.set_ydata(y)
        line.set_color(colors[j % len(colors)])
        line.set_alpha(1)

    return lines

def create_wave_animation():
    """
    Creates a floating Tkinter UI with an animated wave background.
    """
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes("-topmost", True)
    root.configure(bg='white')
    root.attributes("-alpha", 0.8)  # Translucent window
    root.geometry("450x130+1470+30")  # Adjust window position

    # Create a frame with a Royal Blue border
    border_frame = tk.Frame(root, bg="#4169E1", bd=2)
    border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    # Create a figure for the animation
    fig = Figure(figsize=(9, 3), dpi=100, facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])

    x = np.linspace(0, 2, 1000)
    num_waves = 5
    lines = [ax.plot(x, np.sin(2 * np.pi * x), linewidth=3)[0] for _ in range(num_waves)]

    # Setup the grid
    ax.set_xlim(0, 2)
    ax.set_ylim(-1, 1)
    ax.set_facecolor("#FFFFFF")
    ax.grid(color="#4169E1", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.axis('off')

    # Attach the canvas to the frame
    canvas = FigureCanvasTkAgg(fig, master=border_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    ani = animation.FuncAnimation(fig, animate, fargs=(lines, x), frames=200, interval=10, blit=True)

    # Auto-close after 10 seconds
    root.after(10000, root.destroy)
    root.mainloop()
