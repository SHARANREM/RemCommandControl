import tkinter as tk
import win32gui
import win32con
import json
import os
from Brain import Brain

class CheatInput:
    def __init__(self, on_submit):
        self.on_submit = on_submit

        self.root = tk.Tk()
        self.root.withdraw()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        width = 700
        height = 55

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = 20
        y = screen_h - height - 40 

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.frame = tk.Frame(
            self.root,
            bg="black",
            highlightbackground="white",
            highlightthickness=3
        )
       
        
        self.suggestion_box = tk.Listbox(
            self.root,
            bg="black",
            fg="white",
            borderwidth=2,
            highlightbackground="white",
            font=("Consolas", 12)
        )

        self.suggestion_box.place_forget()
        self.frame.pack(fill="both", expand=True)

        self.entry = tk.Entry(
            self.frame,
            bg="black",
            fg="white",
            insertbackground="white",
            borderwidth=0,
            font=("Consolas", 18)
        )

        self.entry.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )
        self.normal_height = 55
        self.expanded_height = 205

        self.original_x = x
        self.original_y = y
        self.entry.bind("<Return>", self.submit)
        self.entry.bind("<Escape>", lambda e: self.hide())
        self.entry.bind("<Up>", self.previous_command)
        self.entry.bind("<Down>", self.next_command)
        self.entry.bind("<KeyRelease>", self.on_text_changed)
        self.entry.bind("<Tab>", self.complete_suggestion)

        self.current_suggestion = ""

        self.history = self.load_history()
        self.history_index = len(self.history)
        self.dropdown_visible = False

    def show_dropdown(self, suggestions):

        if suggestions:
            self.current_suggestion = suggestions[0]
        else:
            self.current_suggestion = ""

        if not self.dropdown_visible:

            self.root.geometry(
                f"700x205+{self.original_x}+{self.original_y-150}"
            )

            self.dropdown_visible = True

        self.suggestion_box.delete(0, tk.END)

        for item in suggestions:
            self.suggestion_box.insert(tk.END, item)

        self.suggestion_box.place(
            x=0,
            y=0,
            width=700,
            height=150
        )

        self.frame.place(
            x=0,
            y=150,
            width=700,
            height=55
        )
            
    def hide_dropdown(self):
        self.current_suggestion = ""

        if self.dropdown_visible:

            self.root.geometry(
                f"700x55+{self.original_x}+{self.original_y}"
            )

            self.dropdown_visible = False

        self.suggestion_box.place_forget()

        self.frame.place(
            x=0,
            y=0,
            width=700,
            height=55
        )

    def complete_suggestion(self, event=None):

        if not self.current_suggestion:
            return "break"

        text = self.entry.get()

        parts = text.split()

        # Command completion
        if len(parts) <= 1:

            self.entry.delete(0, tk.END)
            self.entry.insert(
                0,
                self.current_suggestion
            )

        # Argument completion
        else:

            parts[-1] = self.current_suggestion

            self.entry.delete(0, tk.END)
            self.entry.insert(
                0,
                " ".join(parts)
            )

        return "break"
    
    def on_text_changed(self, event=None):

        text = self.entry.get().strip()

        if text == "":
            self.hide_dropdown()
            return

        suggestions = Brain.get_suggestions(text)

        # print("Suggestions:", suggestions)

        if suggestions:
            self.show_dropdown(suggestions)
        else:
            self.hide_dropdown()

                
    def next_command(self, event=None):

        if not self.history:
            return

        self.history_index = min(
            len(self.history),
            self.history_index + 1
        )

        self.entry.delete(0, tk.END)

        if self.history_index < len(self.history):
            self.entry.insert(
                0,
                self.history[self.history_index]
            )
        else:
            self.entry.delete(0, tk.END)

    def previous_command(self, event=None):

        if not self.history:
            return

        self.history_index = max(
            0,
            self.history_index - 1
        )

        self.entry.delete(0, tk.END)
        self.entry.insert(
            0,
            self.history[self.history_index]
        )

    def load_history(self):

        path = "data/history.json"

        if not os.path.exists(path):
            return []

        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return []
    
    def save_command(self, command):

        self.history.append(command)
        self.history_index = len(self.history)
        os.makedirs("data", exist_ok=True)

        with open("data/history.json", "w") as f:
            json.dump(
                self.history[-100:],
                f,
                indent=4
            )

    def show(self):

        self.root.deiconify()
        self.root.update_idletasks()
        self.history_index = len(self.history)

        hwnd = self.root.winfo_id()

        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE
            | win32con.SWP_NOSIZE
        )

        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            pass

        self.root.lift()

        self.entry.delete(0, tk.END)

        self.entry.focus_force()

        self.root.after(
            200,
            lambda: self.entry.focus_force()
        )

    def hide(self):
        self.root.withdraw()

    def submit(self, event=None):

        text = self.entry.get().strip()

        if text:

            self.save_command(text)

            self.on_submit(text)

        self.hide()

    def run(self):
        self.root.mainloop()