from tkinter import Frame

from PipHome.PipUtils import copy_all_config_to_kw


class PipFrame(Frame):
    def __init__(self, master, config, **kw):
        copy_all_config_to_kw(config, kw, "gui.frame")
        super().__init__(master, **kw)
        self._config = config
