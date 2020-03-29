from tkinter import Listbox


class PipListbox(Listbox):
    def __init__(self, master, config, **kw):
        super().__init__(master, **kw)
        self._config = config
