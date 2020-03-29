from tkinter import Frame


class PipFrame(Frame):
    def __init__(self, master, config, **kw):
        super().__init__(master, **kw)
        self._config = config
