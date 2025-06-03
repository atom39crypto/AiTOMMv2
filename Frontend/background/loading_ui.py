# Frontend/background/loading_ui.py

import tkinter as tk
import math

class LoadingScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading...")
        self.root.geometry("300x300")
        self.root.configure(bg="black")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.center_x = 150
        self.center_y = 150
        self.radius = 60
        self.ball_radius = 15

        self.angle = 0
        self.running = True

        self.colors = ["#9b5de5", "#00bbf9", "#00f5d4", "#5eead4", "#60a5fa"]
        self.color_index = 0

        self.ball = self.canvas.create_oval(
            self.center_x - self.ball_radius,
            self.center_y - self.radius - self.ball_radius,
            self.center_x + self.ball_radius,
            self.center_y - self.radius + self.ball_radius,
            fill="cyan",
            outline=""
        )

    def animate(self):
        if not self.running:
            self.root.destroy()
            return

        self.angle = (self.angle + 3) % 360
        rad = math.radians(self.angle)
        x = self.center_x + self.radius * math.cos(rad)
        y = self.center_y + self.radius * math.sin(rad)

        self.canvas.coords(
            self.ball,
            x - self.ball_radius, y - self.ball_radius,
            x + self.ball_radius, y + self.ball_radius
        )

        self.color_index = (self.color_index + 1) % len(self.colors)
        self.canvas.itemconfig(self.ball, fill=self.colors[self.color_index])

        self.root.after(50, self.animate)

    def run(self):
        self.animate()
        self.root.mainloop()

    def stop(self):
        self.running = False
