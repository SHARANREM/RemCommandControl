import tkinter as tk
import threading
import keyboard
from Brain import Brain
from CheatInput import CheatInput
import sys

cheat_ui = None

def update_ui_status(message, tag="loading"):
    if cheat_ui and cheat_ui.root:
        cheat_ui.root.after(0, lambda: cheat_ui.append_chat(message, tag=tag))

def execute_command_worker(command, had_missing_packages):
    try:
        result = Brain.execute(
            command,
            status_callback=lambda msg: update_ui_status(f"[⚡] {msg}", tag="loading")
        )

        if isinstance(result, dict):
            # Output command list directly into the HUD feed
            if result.get("type") == "help_list":
                text = "=== AVAILABLE COMMANDS ===\n"
                for plugin, data in result["data"].items():
                    text += f"/{plugin:<12} : {data['description']}\n"
                update_ui_status(text.strip(), tag="system")
                return

            # Output specific plugin help directly into the HUD feed
            elif result.get("type") == "help_plugin":
                header = f"=== HELP: /{command.strip().split()[-1]} ==="
                update_ui_status(f"{header}\n{result['data'].strip()}", tag="system")
                return

            elif result.get("success"):
                update_ui_status(f"[✓] Executed: {command}", tag="success")
                
                # If dependencies were installed, close the HUD after finishing
                if had_missing_packages and cheat_ui:
                    cheat_ui.root.after(700, cheat_ui.hide)
                return

    except Exception as e:
        err_msg = f"[!] Error: {e}"
        print(err_msg)
        update_ui_status(err_msg, tag="error")

def on_command(command):
    cleaned = command.strip().lower()

    # Exit command
    if cleaned in ["/exit", "exit", "quit", "/quit"]:
        if cheat_ui:
            cheat_ui.root.destroy()
        sys.exit(0)

    # Check if packages need to be installed or if it's a help command
    missing_packages = Brain.get_missing_packages(command)
    is_help_cmd = cleaned.startswith("/help") or cleaned.startswith("help")

    # If it's a standard command (no missing packages & not help), hide immediately
    if not missing_packages and not is_help_cmd:
        if cheat_ui:
            cheat_ui.hide()
    else:
        if missing_packages:
            update_ui_status(f"[⚡] Dependencies needed: {', '.join(missing_packages)}", tag="loading")

    # Run execution in background worker thread
    threading.Thread(
        target=execute_command_worker,
        args=(command, bool(missing_packages)),
        daemon=True
    ).start()

def activate_cheat_console():
    if cheat_ui:
        cheat_ui.root.after(0, cheat_ui.show)

def register_hotkeys():
    # Toggle with Ctrl + `
    keyboard.add_hotkey("ctrl+`", activate_cheat_console)
    keyboard.wait()

if __name__ == "__main__":
    cheat_ui = CheatInput(on_command)

    threading.Thread(
        target=register_hotkeys,
        daemon=True
    ).start()

    cheat_ui.run()