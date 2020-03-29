from tkinter import Listbox

from PipHome.PipUtils import copy_all_config_to_kw


class PipListbox(Listbox):
    def __init__(self, master, config, **kw):
        copy_all_config_to_kw(config, kw, "gui.listbox")
        super().__init__(master, **kw)
        self._config = config
