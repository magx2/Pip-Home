from tkinter import Button

from PipHome.PipLog import Logger


class PipButton(Button):
    _logger = Logger("PipButton")

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
