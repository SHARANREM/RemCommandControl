# plugins/<PluginName>.py
# ==================================================

# IMPORT RULES

# ==================================================

# If a package appears in required_packages,
# import it INSIDE run().
#
# GOOD:
#
# def run(*args):
#     import requests
#
# BAD:
#
# import requests
#
# Why?
#
# RemCheatControl reads plugin metadata
# before installing packages.
#
# Top-level imports can crash loading.

# ==================================================

# FILE NAME = <PluginName? = COMMAND NAME

# ==================================================

# Example:
# browse.py  ->  /browse
# open.py    ->  /open
# So choose wisely.
# Because renaming files later is basically
# admitting your past self had bad ideas.

description = """
Short description shown in /help.
Keep it short.
Humans fear reading.
"""

# ==================================================

# HELP TEXT

# ==================================================

# Used in:
# /help <PluginName>
# This is where you explain:
# - syntax
# - examples
# - arguments

# If users don't read this,
# they will randomly press keys
# and report bugs that are actually features.

help = """
Plugin Name

Usage:
/plugin something

Examples:
/plugin hello

Arguments:
hello - does something

Description:
Explain what this plugin does.
"""

# ==================================================

# REQUIRED PACKAGES

# ==================================================

# ONLY packages installed through pip belong here.
#
# Good:
# requests
# pyautogui
# pillow
# beautifulsoup4
#
# Bad:
# os
# sys
# json
# subprocess
# threading
# tkinter
#
# Built-in Python modules DO NOT belong here.
#
# RemCheatControl automatically installs
# anything listed below.

required_packages = []

# Example:
#
# required_packages = [
#     "requests",
#     "beautifulsoup4"
# ]

# ==================================================

# AUTOCOMPLETE SUGGESTIONS

# ==================================================
# These appear in the dropdown.
# Example:
# /browse g
# Suggests:
# github
# Without autocomplete,
# users become explorers searching
# for lost civilizations.


suggestions = [
"example1",
"example2",
"example3"
]

# ==================================================

# OPTIONAL DATA

# ==================================================
# # Store reusable stuff here.
# URLs
# App paths
# Configs
# Nuclear launch codes
# (Preferably not the last one.)
DATA = {
"example1": "value1",
"example2": "value2"
}

# ==================================================

# MAIN FUNCTION

# ==================================================

# RemCheatControl always calls:
# run(*args)

# Example:
# /plugin hello

# becomes:
# args = ("hello",)
# /plugin hello world

# becomes:
# args = ("hello", "world")
# If this function crashes,
# the plugin achieves enlightenment
# and leaves this mortal realm.

def run(*args):
    pass

# ----------------------------------------------
# Validate arguments
# ----------------------------------------------
#
# Users will absolutely forget arguments.
# It is their destiny.

'''
if not args:
    raise Exception(
        "Missing argument. Use /help plugin"
    )
'''

# ----------------------------------------------
# First argument
# ----------------------------------------------
#
# Usually the main command target.

#command = args[0].lower()

# ----------------------------------------------
# Validate command
# ----------------------------------------------
#
# Prevent chaos.
# Chaos is fun until production.
'''
if command not in DATA:
    raise Exception(
        f"Unknown command '{command}'"
    )
'''

# ----------------------------------------------
# Main plugin logic
# ----------------------------------------------

# Replace this section with actual code.

#value = DATA[command]
'''
print(
    f"Running command: {command}"
)
'''

# ----------------------------------------------
# Return result (optional)
# ----------------------------------------------
#
# Useful for:
# - Notifications
# - Logs
# - Future UI
# - Evidence that the plugin actually worked
'''
return {
    "success": True,
    "command": command,
    "value": value
}
'''
# ==================================================

# THREAD WARNING

# ==================================================

# Plugins now run as separate processes.
#
# This means:
#
# GOOD:
#
# /notify 10 hello
#
# Plugin sleeps 10 seconds
# then shows popup.
#
# BAD:
#
# Start daemon thread
# Return immediately
#
# Because the process exits
# and the thread dies with it.
#
# If the plugin needs to stay alive:
#
# Keep run() alive.
#
# Do NOT launch a daemon thread
# and immediately return.

# ==================================================

# ENTRY POINT

# ==================================================

# Required for RemCheatControl.
#
# Allows the plugin to run
# as an independent process.

if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])

'''
Full Example
# plugins/countdown.py

import tkinter as tk
import threading
import time

description = "Countdown timer"

required_packages = []

help = """
Usage:
/countdown 5

Starts a 5 minute countdown.
"""
suggestions = [
    "25",
    "5"
]

def timer_window(seconds):

    root = tk.Tk()

    root.overrideredirect(True)
    root.attributes("-topmost", True)

    width = 240
    height = 80

    screen_w = root.winfo_screenwidth()

    root.geometry(
        f"{width}x{height}+{screen_w-width-20}+20"
    )

    frame = tk.Frame(
        root,
        bg="black",
        highlightbackground="white",
        highlightthickness=2
    )

    frame.pack(fill="both", expand=True)

    label = tk.Label(
        frame,
        bg="black",
        fg="white",
        font=("Consolas", 32, "bold")
    )

    label.pack(expand=True)

    def update():

        remaining = seconds

        while remaining >= 0:

            mins = remaining // 60
            secs = remaining % 60

            label.config(
                text=f"{mins:02}:{secs:02}"
            )

            root.update()

            time.sleep(1)

            remaining -= 1

        root.destroy()

    threading.Thread(
        target=update,
        daemon=True
    ).start()

    root.mainloop()


def run(*args):

    if not args:
        raise Exception(
            "Missing minute value"
        )

    minutes = int(args[0])

    timer_window(
        minutes * 60
    )

if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])


Another one
# plugins/browse.py

import subprocess

description = """
Opens saved links in your default browser.
"""

suggestions = [
    "github",
    "yt",
    "chatgpt"
]

help = """
Browse saved links.

Usage:
/browse github
/browse yt
/browse chatgpt

Examples:
/browse github
/browse yt

Description:
Opens predefined URLs using your default browser.
"""

required_packages = []

LINKS = {
    "github": "https://github.com",
    "yt": "https://youtube.com",
    "chatgpt": "https://chatgpt.com"
}

def run(*args):

    if not args:
        raise Exception(
            "Missing link name"
        )

    key = args[0].lower()

    if key not in LINKS:
        raise Exception(
            f"Unknown link '{key}'"
        )

    subprocess.Popen(
        ["cmd", "/c", "start", LINKS[key]],
        shell=True
    )

    return {
        "success": True,
        "message": f"Opened {key}"
    }

if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])


    
'''


