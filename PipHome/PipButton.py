from tkinter import Button

from PipHome.PipLog import Logger


class PipButton(Button):
    _logger = Logger("PipButton")

    def __init__(self, master, config, **kw):
        super().__init__(master, **kw)
        self._config = config
