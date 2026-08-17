
import time

description = """
Set a timer that shows a popup notification with sound
"""

required_packages = []

help = """
Notify Plugin

Usage:
/notify 10 Hello
/notify 5 Take a break
"""

suggestions = [
    "5 break",
    "10 focus",
    "30 rest"
]


def show_alert(message):
    import winsound
    winsound.Beep(
        1000,
        500
    )

    import tkinter as tk

    root = tk.Tk()

    root.title("Reminder")
    root.geometry(
        "300x120+800+400"
    )

    root.configure(
        bg="black"
    )

    root.attributes(
        "-topmost",
        True
    )

    label = tk.Label(
        root,
        text=message,
        fg="white",
        bg="black",
        font=("Consolas", 12),
        wraplength=280
    )

    label.pack(
        expand=True
    )

    root.after(
        4000,
        root.destroy
    )

    root.mainloop()


def run(*args):

    if not args:
        raise Exception(
            "Usage: /notify <seconds> <message>"
        )

    try:

        seconds = int(args[0])

    except:

        raise Exception(
            "First argument must be time in seconds"
        )

    message = (
        " ".join(args[1:])
        if len(args) > 1
        else "Reminder!"
    )

    time.sleep(seconds)

    show_alert(message)


if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])