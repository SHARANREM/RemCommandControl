# plugins/open.py

import subprocess

description = "Open applications"

required_packages = []

help = """
Usage:
/open chrome
/open notepad
/open vscode

Opens a predefined application.
"""
suggestions = [
    "chrome",
    "notepad",
    "vscode"
]
APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "vscode": r"C:\Users\YOUR_USER\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}


def run(*args):

    if not args:
        raise Exception("Missing app name")

    app = args[0].lower()

    if app not in APPS:
        raise Exception(f"Unknown app '{app}'")

    subprocess.Popen(APPS[app])

    return {
        "success": True,
        "message": f"Opened {app}"
    }

if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])