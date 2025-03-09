import tkinter as tk
from tkinter import ttk


class EntryWithlabel(ttk.Frame):
    def __init__(self, master: tk.Misc, label: str = None, default: str = "", secret: bool = False, **kwargs) -> None:
        super().__init__(master)

        if label is not None:
            self.label = ttk.Label(self, text=label, foreground="grey")
            self.label.pack(side="top", anchor="w")

        show = "*" if secret else ""
        self.entry = ttk.Entry(self, show=show, **kwargs)
        self.entry.insert(0, default)
        self.entry.pack(side="bottom", fill="x")

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, value)