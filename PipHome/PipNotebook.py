from tkinter import TOP, X, BOTH, BOTTOM, LEFT

from PipHome.PipButton import PipButton
from PipHome.PipFrame import PipFrame
from PipHome.PipLog import Logger


class PipNotebook(PipFrame):
    _logger = Logger("PipNotebook", level="DEBUG")
    _tabs = {}
    _active = None

    def __init__(self, master, config, **kw):
        super().__init__(master, config, **kw)
        self._build_buttons()
        self._build_content()

    def _build_buttons(self):
        self._buttons = PipFrame(self, self._config, bg="blue")
        self._buttons.pack(side=TOP, fill=X, padx=5, pady=5)

    def _build_content(self):
        self._content = PipFrame(self, self._config, bg="cyan")
        self._content.pack(side=BOTTOM, fill=BOTH, expand=1, padx=5, pady=5)

    def add(self, pip_tab, **kw):
        text = kw["text"]
        button = PipButton(self._buttons,
                           self._config,
                           text=kw["text"],
                           command=lambda: self._button_clicked(text))
        self._tabs[text] = (pip_tab, button)
        button.pack(side=LEFT, padx=2)
        if len(self._tabs) <= 1:
            self._button_clicked(text)

    def _button_clicked(self, button_name):
        if self._active is not None:
            self._logger.debug("Removing old tab")
            self._active[0].hide()
            self._active[1].config(background=self._config["gui.button.background"],
                                   foreground=self._config["gui.button.foreground"])
        self._logger.debug(f"Loading tab `{button_name}`")
        (tab, button) = self._tabs[button_name]
        tab.render(self._content)
        self._active = (tab, button)
        button.config(background=self._config["gui.button.foreground"],
                      foreground=self._config["gui.button.background"])
