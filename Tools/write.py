import os
from docx import Document

def write_word(file_name, content):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_name)
    print(f"Word document '{file_name}' has been created!")

def write_code(file_name, content):
    with open(file_name, "w") as file:
        file.write(content)
    print(f"'{file_name}' has been created successfully.")

def get_desktop_folder():
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")  # For Windows
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")  # For macOS/Linux
    return desktop

import os
import subprocess
import platform

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", path])
    else:  # Linux
        subprocess.call(["xdg-open", path])

def write(a, b):
    print("<-------------------------- generating the file --------------------------->")

    current_dir = os.getcwd()
    output_folder = os.path.join(current_dir, "Generated_Files")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, a)

    if a.endswith(".docx"):
        write_word(file_path, b)
    else:
        write_code(file_path, b)

    open_file(file_path)
    return "file created and opened"



if __name__ == "__main__":
    write("aslhkflkhasflhas.py", "print('Hello, world!')")  
    write("new.docx", "This is content for the Word file.")  