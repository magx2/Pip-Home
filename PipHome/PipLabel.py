from tkinter import ttk


class PipLabel(ttk.Label):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
