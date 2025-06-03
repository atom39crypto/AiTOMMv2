import subprocess


def launch_third_terminal(a):
    a = a.replace(" ", "_")
    with open("run3.bat", "w") as f:
        f.write(rf"""@echo off
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
call .\AiTOMM\Scripts\activate.bat
python ImageGenarator.py {a}
pause
""")
    subprocess.Popen("start cmd /k run3.bat", shell=True)
    return "Image Genarator is running in another terminal, please check it."+a


if __name__ == "__main__":
    # Test the function with a sample prompt
    # launch_third_terminal("test and life")
    # subprocess.Popen("start cmd /k run3.bat", shell=True)

    print(launch_third_terminal("alter Image background to yellow"))