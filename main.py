import tkinter as tk
import threading
import keyboard
from Brain import Brain
from CheatInput import CheatInput
from HelpPanel import HelpPanel
import sys

# print(sys.executable)
# print(sys.version)
# print(sys.platform)
cheat_ui = None
help_panel = HelpPanel()

def show_cheat_notification(text):

    popup = tk.Toplevel()

    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    width = 300
    height = 50

    popup.geometry(f"{width}x{height}+20+20")

    label = tk.Label(
        popup,
        text=f"CHEAT ACTIVATED",
        bg="black",
        fg="white",
        font=("Arial", 10, "bold")
    )

    label.pack(fill="both", expand=True)

    alpha = 1.0

    def fade():
        nonlocal alpha

        if alpha > 0:
            alpha -= 0.05
            popup.attributes("-alpha", alpha)
            popup.after(50, fade)
        else:
            popup.destroy()

    popup.after(1200, fade)


def on_command(command):

    try:

        # =====================================
        # EXIT COMMAND
        # =====================================

        if command.strip().lower() in [
            "/exit",
            "exit"
        ]:

            # print(
            #     "RemCheatControl shutting down..."
            # )

            cheat_ui.root.destroy()

            sys.exit(0)

        result = Brain.execute(command)

        if isinstance(result, dict):

            if result.get("type") == "help_list":

                text = ""

                for plugin, data in result["data"].items():

                    text += (
                        f"{plugin}\n"
                        f"  {data['description']}\n\n"
                    )

                help_panel.show(
                    "AVAILABLE COMMANDS",
                    text
                )

                return

            elif result.get("type") == "help_plugin":

                help_panel.show(
                    "PLUGIN HELP",
                    result["data"]
                )

                return

        show_cheat_notification(command)

    except Exception as e:

        print("ERROR:", e)


def activate_cheat_console():
    cheat_ui.root.after(
        0,
        cheat_ui.show
    )


def register_hotkeys():
    keyboard.add_hotkey(
        "ctrl+`",
        activate_cheat_console
    )

    keyboard.wait()


if __name__ == "__main__":

    cheat_ui = CheatInput(on_command)

    threading.Thread(
        target=register_hotkeys,
        daemon=True
    ).start()

    cheat_ui.run()