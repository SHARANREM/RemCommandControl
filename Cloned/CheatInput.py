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

        # Frameless, full-screen HUD overlay with dark glass transparency
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#0a0a0c")
        self.root.attributes("-alpha", 0.85)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_w}x{self.screen_h}+0+0")

        # Dismiss when clicking background
        self.root.bind("<Button-1>", self.on_background_click)

        # Minecraft style root padding
        self.main_container = tk.Frame(self.root, bg="#0a0a0c")
        self.main_container.pack(fill="both", expand=True, padx=25, pady=25)

        # ----------------------------------------------------
        # TOP/CENTER: Upward Scrolling Chat Feed (NO SCROLLBAR)
        # ----------------------------------------------------
        self.chat_frame = tk.Frame(self.main_container, bg="#0d0d11")
        self.chat_frame.pack(fill="both", expand=True, side="top", pady=(0, 6))

        self.chat_box = tk.Text(
            self.chat_frame,
            bg="#0d0d11",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            font=("Consolas", 13),
            wrap="word",
            padx=16,
            pady=16,
            cursor="arrow"
        )
        self.chat_box.pack(fill="both", expand=True)

        # Minecraft chat color tags
        self.chat_box.tag_config("system", foreground="#55FFFF")
        self.chat_box.tag_config("command", foreground="#FFAA00", font=("Consolas", 13, "bold"))
        self.chat_box.tag_config("success", foreground="#55FF55")
        self.chat_box.tag_config("loading", foreground="#FFFF55", font=("Consolas", 13, "italic"))
        self.chat_box.tag_config("error", foreground="#FF5555")
        self.chat_box.tag_config("dim", foreground="#AAAAAA")
        self.chat_box.config(state="disabled")

        # ----------------------------------------------------
        # SUGGESTIONS BAR (Minecraft-style Tab Auto-Complete Bar)
        # ----------------------------------------------------
        self.suggestion_bar = tk.Frame(self.main_container, bg="#0a0a0c")
        self.suggestion_bar.pack(fill="x", side="top", pady=(0, 6))
        self.current_suggestions = []

        # ----------------------------------------------------
        # BOTTOM: Input Bar & Enter Button
        # ----------------------------------------------------
        self.input_wrapper = tk.Frame(
            self.main_container,
            bg="#141419",
            highlightbackground="#555555",
            highlightcolor="#FFFFFF",
            highlightthickness=2
        )
        self.input_wrapper.pack(fill="x", side="bottom")

        self.prompt_label = tk.Label(
            self.input_wrapper,
            text=" > ",
            bg="#141419",
            fg="#55FFFF",
            font=("Consolas", 16, "bold")
        )
        self.prompt_label.pack(side="left", padx=(10, 0))

        self.entry = tk.Entry(
            self.input_wrapper,
            bg="#141419",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            borderwidth=0,
            font=("Consolas", 15)
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=8, pady=10)

        # Bottom-right ENTER Button
        self.enter_btn = tk.Button(
            self.input_wrapper,
            text="ENTER ↵",
            bg="#2a2a35",
            fg="#FFFFFF",
            activebackground="#4a4a5a",
            activeforeground="#55FF55",
            relief="flat",
            font=("Consolas", 12, "bold"),
            padx=18,
            pady=6,
            cursor="hand2",
            command=self.submit
        )
        self.enter_btn.pack(side="right", padx=10, pady=8)

        # Keybindings
        self.entry.bind("<Return>", self.submit)
        self.entry.bind("<Escape>", lambda e: self.hide())
        self.entry.bind("<Up>", self.previous_command)
        self.entry.bind("<Down>", self.next_command)
        self.entry.bind("<KeyRelease>", self.on_text_changed)
        self.entry.bind("<Tab>", self.complete_suggestion)
        self.root.bind("<Escape>", lambda e: self.hide())

        self.history = self.load_history()
        self.history_index = len(self.history)

        self.append_chat("RemCheatControl HUD Initialized. Press ESC to close, Ctrl+` to toggle.", tag="system")

    def on_background_click(self, event):
        widget = event.widget
        if widget == self.root or widget == self.main_container:
            self.hide()

    def append_chat(self, text, tag="dim"):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, text + "\n", tag)
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def show_suggestions(self, suggestions):
        self.current_suggestions = suggestions
        for widget in self.suggestion_bar.winfo_children():
            widget.destroy()

        if not suggestions:
            return

        for s in suggestions[:8]:
            btn = tk.Button(
                self.suggestion_bar,
                text=s,
                bg="#1a1a24",
                fg="#FFFF55",
                activebackground="#33334d",
                activeforeground="#FFFFFF",
                font=("Consolas", 11),
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda val=s: self.apply_suggestion(val)
            )
            btn.pack(side="left", padx=4)

    def hide_suggestions(self):
        self.current_suggestions = []
        for widget in self.suggestion_bar.winfo_children():
            widget.destroy()

    def apply_suggestion(self, suggestion):
        text = self.entry.get()
        parts = text.split()

        if len(parts) <= 1:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, suggestion + " ")
        else:
            parts[-1] = suggestion
            self.entry.delete(0, tk.END)
            self.entry.insert(0, " ".join(parts) + " ")

        self.entry.focus_set()
        self.on_text_changed()

    def complete_suggestion(self, event=None):
        if not self.current_suggestions:
            return "break"

        self.apply_suggestion(self.current_suggestions[0])
        return "break"

    def on_text_changed(self, event=None):
        text = self.entry.get().strip()

        if not text:
            self.hide_suggestions()
            return

        suggestions = Brain.get_suggestions(text)
        if suggestions:
            self.show_suggestions(suggestions)
        else:
            self.hide_suggestions()

    def next_command(self, event=None):
        if not self.history:
            return

        self.history_index = min(len(self.history), self.history_index + 1)
        self.entry.delete(0, tk.END)

        if self.history_index < len(self.history):
            self.entry.insert(0, self.history[self.history_index])
        else:
            self.entry.delete(0, tk.END)
        self.on_text_changed()

    def previous_command(self, event=None):
        if not self.history:
            return

        self.history_index = max(0, self.history_index - 1)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.history[self.history_index])
        self.on_text_changed()

    def load_history(self):
        path = os.path.join("data", "history.json")
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save_command(self, command):
        self.history.append(command)
        self.history_index = len(self.history)
        os.makedirs("data", exist_ok=True)
        try:
            with open(os.path.join("data", "history.json"), "w") as f:
                json.dump(self.history[-100:], f, indent=4)
        except Exception:
            pass

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
            self.screen_w,
            self.screen_h,
            win32con.SWP_SHOWWINDOW
        )
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass

        self.root.lift()
        self.entry.focus_force()
        self.root.after(100, lambda: self.entry.focus_force())

    def hide(self):
        self.hide_suggestions()
        self.root.withdraw()

    def submit(self, event=None):
        text = self.entry.get().strip()
        if text:
            self.save_command(text)
            self.append_chat(f"> {text}", tag="command")
            self.entry.delete(0, tk.END)
            self.hide_suggestions()
            self.on_submit(text)

    def run(self):
        self.root.mainloop()