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