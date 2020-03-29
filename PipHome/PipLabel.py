from tkinter import *

from PipHome.PipUtils import copy_all_config_to_kw


class PipLabel(Label):
    def __init__(self, master, config, **kw):
        copy_all_config_to_kw(config, kw, "gui.label")
        super().__init__(master, **kw)
        self._config = config
