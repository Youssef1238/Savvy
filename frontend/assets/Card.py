import tkinter as tk
from tkinter import ttk

class Card(ttk.Frame):
    def __init__(self, parent, title, content, command=None, *args, **kwargs):
        super().__init__(parent,style="Card.TFrame", *args, **kwargs)
                  



        self.title_label = ttk.Label(self, text=title,style="CardTitle.TLabel")
        self.title_label.pack(pady=(10, 5), padx=10, anchor="w")


        self.content_label = ttk.Label(self, text=content,style="Card.TLabel",wraplength=500)
        self.content_label.pack(pady=(0, 10), padx=10, anchor="w")

        self.bind("<Enter>", lambda e: self.state("hover"))
        self.bind("<Leave>", lambda e: self.state("!hover"))
        self.bind("<Button-1>", lambda e: command() if command else None)


        for widget in self.winfo_children():
            widget.bind("<Enter>", lambda e: self.state("hover"))
            widget.bind("<Leave>", lambda e: self.state("!hover"))
            widget.bind("<Button-1>", lambda e: command() if command else None)

    def state(self, state):
        self.state_set = state
        if state == "hover":
            self.configure(style="hoverCard.TFrame")
            self.title_label.configure(background="#b66b16")
            self.title_label.configure(foreground="white")
            self.content_label.configure(background="#b66b16")
        elif state == "!hover":
            self.configure(style="Card.TFrame")
            self.title_label.configure(background="#333333")
            self.title_label.configure(foreground="#b66b16")
            self.content_label.configure(background="#333333")

