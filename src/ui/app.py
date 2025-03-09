import os
import json
import threading
import tkinter as tk
import sv_ttk as svtk  # Only used to set the theme
from tkinter import ttk
from datetime import datetime

from bot import Bot
from ui.entry_with_label import EntryWithlabel


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Promocode Scraper")
        self.geometry("800x460")
        self.minsize(800, 460)

        self.setup_ui()

        self.bot = None

    def run(self) -> None:
        """Runs the application."""

        svtk.set_theme("light")
        self.load_config()
        
        self.bot = Bot(self)
        self.mainloop()
        
    def destroy(self):
        self.save_config()
        super().destroy()

    def get_values(self) -> dict:
        """Returns the configuration values from the UI."""

        return {
            "x_auth_token": self.x_auth_token.get(),
            "x_csrf_token": self.x_csrf_token.get(),
            "discord_api_key": self.discord_api_key.get(),
            "discord_webhook": self.discord_webhook.get(),
            "dark_mode": self.dark_mode.get(),
            "start_with_os": self.start_with_os.get(),
            "start_minimized": self.start_minimized.get()
        }

    def save_config(self) -> None:
        """Saves the configuration values to a file."""

        if not os.path.exists("data"):
            os.makedirs("data")

        with open("data/config.json", "w") as file:
            json.dump(self.get_values(), file, indent=2)

    def load_config(self) -> None:
        """Loads the configuration values from a file."""

        if not os.path.exists("data/config.json"):
            return

        with open("data/config.json", "r") as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError:
                return

            self.x_auth_token.set(config["x_auth_token"])
            self.x_csrf_token.set(config["x_csrf_token"])
            self.discord_api_key.set(config["discord_api_key"])
            self.discord_webhook.set(config["discord_webhook"])

            self.dark_mode.set(config["dark_mode"])
            self.start_with_os.set(config["start_with_os"])
            self.start_minimized.set(config["start_minimized"])

            svtk.set_theme("dark" if config["dark_mode"] else "light")

    def force_start(self) -> None:
        """Starts the scraping process in a separate thread to prevent freezing."""

        threading.Thread(target=self.bot.run).start()

    def setup_ui(self) -> None:
        """Initialize and arrange all UI components."""

        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True)
        
        self.create_options_section(left_frame)
        self.create_credentials_section(left_frame)
        self.create_start_button(left_frame)

        right_frame = ttk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        self.create_log_section(right_frame)

    def create_credentials_section(self, frame: tk.Frame) -> None:
        """Creates the credentials input section."""
        
        credentials_frame = ttk.LabelFrame(frame, text="Credentials")
        credentials_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.x_auth_token = EntryWithlabel(credentials_frame, label="X Auth Token", secret=True)
        self.x_auth_token.pack(fill="x", padx=10, pady=5)

        self.x_csrf_token = EntryWithlabel(credentials_frame, label="X CSRF Token", secret=True)
        self.x_csrf_token.pack(fill="x", padx=10, pady=5)

        self.discord_api_key = EntryWithlabel(credentials_frame, label="Discord API Key", secret=True)
        self.discord_api_key.pack(fill="x", padx=10, pady=5)

        self.discord_webhook = EntryWithlabel(credentials_frame, label="Discord Webhook URL (Optional)", secret=True)
        self.discord_webhook.pack(fill="x", padx=10, pady=5)

    def create_options_section(self, frame: tk.Frame) -> None:
        """Creates the options section."""
        
        options_frame = ttk.LabelFrame(frame, text="Options")
        options_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.dark_mode = tk.BooleanVar(value=False)
        self.chk_dark_mode = ttk.Checkbutton(
            options_frame,
            text="Dark Mode",
            variable=self.dark_mode,
            style="Switch.TCheckbutton",
            command=lambda: svtk.set_theme("dark" if self.dark_mode.get() else "light")
        )
        self.chk_dark_mode.pack(fill="x", padx=10, pady=5)

        self.start_with_os = tk.BooleanVar(value=True)
        self.chk_start_with_os = ttk.Checkbutton(
            options_frame,
            text="Start with OS",
            variable=self.start_with_os,
            style="Switch.TCheckbutton",
            command=lambda: print(self.start_with_os.get()) # TODO: Implement
        )
        self.chk_start_with_os.pack(fill="x", padx=10, pady=5)

        self.start_minimized = tk.BooleanVar(value=True)
        self.chk_start_minimized = ttk.Checkbutton(
            options_frame,
            text="Start Minimized",
            variable=self.start_minimized,
            style="Switch.TCheckbutton",
            command=lambda: print(self.start_minimized.get()) # TODO: Implement
        )
        self.chk_start_minimized.pack(fill="x", padx=10, pady=5)

    def create_start_button(self, frame: tk.Frame) -> None:
        """Creates the start button."""
        
        start_button = ttk.Button(frame, text="Force Start", command=self.force_start, style="Accent.TButton")
        start_button.pack(fill="x", padx=10, pady=10)

    def create_log_section(self, frame: tk.Frame) -> None:
        """Creates the log section."""
        
        log_frame = ttk.LabelFrame(frame, text="Log")
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.log_section = tk.Text(log_frame, wrap="word", state="disabled", bd=0, font=("Consolas", 10))
        self.log("Promocode Scraper has started")
        self.log_section.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, message: str, end: str = "\n", prefix: str = f"[{datetime.now().strftime('%H:%M:%S')}] ") -> None:
        """Logs a message to the log section."""
        
        self.log_section.config(state="normal")
        self.log_section.insert(tk.END, f"{prefix}{message}{end}")
        self.log_section.config(state="disabled")
        self.log_section.see(tk.END)
