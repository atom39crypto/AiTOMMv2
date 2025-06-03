import os
import tkinter as tk
from tkinter import filedialog

# Hide the root window
def uploder():
    root = tk.Tk()
    root.withdraw()

# Open file dialog
    file_path = filedialog.askopenfilename()
    print("Selected file path:", file_path)

# Get directory
    directory = os.path.dirname(file_path)

# Get file name
    file_name = os.path.basename(file_path)

# Get file name without extension
    file_name_wo_ext = os.path.splitext(file_name)[0]

    return file_path #, directory, file_name, file_name_wo_ext
