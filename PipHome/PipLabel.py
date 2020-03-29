from tkinter import *


class PipLabel(Label):
    def __init__(self, master, config, **kw):
        kw["background"] = config["gui.label.background"]
        kw["foreground"] = config["gui.label.foreground"]
        super().__init__(master, **kw)
        self._config = config
