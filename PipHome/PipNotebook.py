from tkinter import TOP, X, BOTH, BOTTOM, LEFT

from PipHome.PipButton import PipButton
from PipHome.PipFrame import PipFrame
from PipHome.PipLog import Logger


class PipNotebook(PipFrame):
    _logger = Logger("PipNotebook", level="DEBUG")
    _tabs = {}

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._actual_tab = None
        self._build_buttons()
        self._build_content()

    def _build_buttons(self):
        self._buttons = PipFrame(self, bg="blue")
        self._buttons.pack(side=TOP, fill=X)

    def _build_content(self):
        self._content = PipFrame(self, bg="cyan")
        self._content.pack(side=BOTTOM, fill=BOTH, expand=1)

    def add(self, pip_tab, **kw):
        text = kw["text"]
        button = PipButton(self._buttons, text=kw["text"], command=lambda: self._button_clicked(text))
        self._tabs[text] = pip_tab
        button.pack(side=LEFT)
        if len(self._tabs) <= 1:
            self._button_clicked(text)

    def _button_clicked(self, button_name):
        if self._actual_tab is not None:
            self._logger.debug("Removing old tab")
            self._actual_tab.pack_forget()
        self._logger.debug(f"Loading tab `{button_name}`")
        tab = self._tabs[button_name]
        self._actual_tab = tab.render(self._content)
