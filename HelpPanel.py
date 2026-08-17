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

        width = 700
        height = 400

        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

        frame = tk.Frame(
            self.window,
            bg="black",
            highlightbackground="white",
            highlightthickness=3
        )

        frame.pack(
            fill="both",
            expand=True
        )

        title_label = tk.Label(
            frame,
            text=title,
            bg="black",
            fg="white",
            font=("Consolas", 18, "bold")
        )

        title_label.pack(
            pady=(15, 10)
        )

        text = tk.Text(
            frame,
            bg="black",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Consolas", 12),
            wrap="word"
        )

        text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        text.insert("1.0", content)

        text.config(state="disabled")

        footer = tk.Label(
            frame,
            text="ESC to close",
            bg="black",
            fg="white",
            font=("Consolas", 10)
        )

        footer.pack(
            pady=(0, 10)
        )

        self.window.bind(
            "<Escape>",
            lambda e: self.close()
        )

        self.window.bind(
            "<Return>",
            lambda e: self.close()
        )

        self.window.focus_force()

    def close(self):

        if self.window and self.window.winfo_exists():
            self.window.destroy()