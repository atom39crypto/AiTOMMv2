import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import threading
import gc
from Core.AI import mainframe
from Frontend.background.TTS_ui import run_tts_app
from Mainframe.simple_tools import services
# Global variable for the Tkinter root window.
root = None

def animate(i, lines, x):
    colors = ["#8A2BE2", "#6A5ACD", "#4169E1", "#1E90FF", "#00BFFF"]  # Purple to Blue gradient
    for j, line in enumerate(lines):
        phase_shift = j * 0.2  # Staggered movement
        amplitude = 0.4 - (j * 0.05)  # Reduced amplitude for a cleaner look
        y = -0.4 + amplitude * np.sin(2 * np.pi * (x - 0.01 * i) + phase_shift)  # Shift waves downward
        line.set_ydata(y)
        line.set_color(colors[j % len(colors)])
        line.set_alpha(1)  # Fully opaque lines
    return lines

def create_wave_animation(prompt_text):
    global root
    try:
        root = tk.Tk()
        root.overrideredirect(True)  # Remove window decorations
        root.attributes("-topmost", True)
        root.configure(bg='white')
        root.attributes("-alpha", 0.8)  # Translucent window
        root.geometry("450x130+1470+30")  # Adjust window size and position

        # Create a frame that serves as a Royal Blue border
        border_frame = tk.Frame(root, bg="#4169E1", bd=2)  # Royal Blue border
        border_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create a figure with white background for the plot area
        fig = Figure(figsize=(9, 3), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_position([0, 0, 1, 1])  # Fill the entire figure
        
        # Add the prompt text ABOVE the sound wave, fully visible
        ax.text(0.5, 0.75, prompt_text, transform=ax.transAxes,
                fontsize=14, color="black", ha='center', va='center', weight='bold')

        x = np.linspace(0, 2, 1000)
        num_waves = 5  # Multiple overlapping waves
        lines = [ax.plot(x, np.sin(2 * np.pi * x), linewidth=3)[0] for _ in range(num_waves)]
        
        # Configure the plot
        ax.set_xlim(0, 2)
        ax.set_ylim(-1, 1)
        ax.set_facecolor("#FFFFFF")
        ax.grid(color="#4169E1", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.axis('off')

        # Embed the figure in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=border_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Start the animation; it will run until root.destroy() is called.
        ani = animation.FuncAnimation(fig, animate, fargs=(lines, x), frames=200, interval=10, blit=True)

        root.mainloop()
    
    except Exception as e:
        print(f"Error in UI: {e}")

    finally:
        # Ensure Tkinter is fully cleaned up
        try:
            if root:
                root.quit()
                root.destroy()
        except Exception as cleanup_error:
            print(f"Cleanup Error: {cleanup_error}")

        # Reset Tkinter's default root to avoid reference issues
        tk._default_root = None

        # Force garbage collection to clean up lingering Tkinter objects
        gc.collect()

def allCommands(prompt="halo"):
    response_holder = []

    def run_mainframe():
        if prompt in ["shut up", "stop", "quiet"]:
            print("Stopping...")
            if root:
                root.after(0, root.destroy)
            return
        response = services(prompt)
        response_holder.append(response)
        if root:
            root.after(0, root.destroy)

    # Start the mainframe function in a separate thread
    mainframe_thread = threading.Thread(target=run_mainframe)
    mainframe_thread.start()

    # Run the wave animation (blocks until the window is closed)
    create_wave_animation(prompt)

    # Ensure the mainframe thread has finished
    mainframe_thread.join()

    # Now that the wave UI is fully closed, call run_tts_app with the response.
    if response_holder:
        run_tts_app(response_holder[0])

if __name__ == "__main__":
    allCommands("halo")
