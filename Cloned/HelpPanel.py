import tkinter as tk

class HelpPanel:
    def __init__(self):
        self.window = None

    def show(self, title, content):
        if self.window and self.window.winfo_exists():
            self.window.destroy()

        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#0a0a0c")
        self.window.attributes("-alpha", 0.92)

        width = 750
        height = 480

        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        frame = tk.Frame(
            self.window,
            bg="#111116",
            highlightbackground="#55FFFF",
            highlightthickness=2
        )
        frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            frame,
            text=f"§e {title} §r",
            bg="#111116",
            fg="#FFFF55",
            font=("Consolas", 16, "bold")
        )
        title_label.pack(pady=(15, 8))

        text_widget = tk.Text(
            frame,
            bg="#0b0b0e",
            fg="#E0E0E0",
            insertbackground="#FFFFFF",
            relief="flat",
            font=("Consolas", 12),
            wrap="word",
            padx=15,
            pady=10
        )
        text_widget.pack(fill="both", expand=True, padx=15, pady=5)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

        footer = tk.Label(
            frame,
            text="[ ESC / ENTER to close ]",
            bg="#111116",
            fg="#888888",
            font=("Consolas", 10)
        )
        footer.pack(pady=(5, 10))

        self.window.bind("<Escape>", lambda e: self.close())
        self.window.bind("<Return>", lambda e: self.close())
        self.window.focus_force()

    def close(self):
        if self.window and self.window.winfo_exists():
            self.window.destroy()