from tkinter import Listbox


class PipListbox(Listbox):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
