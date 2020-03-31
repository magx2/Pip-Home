from tkinter import Button

from PipHome.PipLog import Logger
from PipHome.PipUtils import copy_all_config_to_kw


class PipButton(Button):
    _logger = Logger("PipButton")

    def __init__(self, master, config, **kw):
        copy_all_config_to_kw(config, kw, "gui.button")
        super().__init__(master, **kw)
        self._config = config
