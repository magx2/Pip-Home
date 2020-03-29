from tkinter import RIGHT

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipLog import Logger


class PipStatusBar(PipFrame):
    _logger = Logger("PipStatusBar")

    def __init__(self, master, config, **kw):
        super().__init__(master, config, **kw)
        # battery
        self._battery = PipLabel(self, self._config, text="100%")
        self._battery.pack(side="right")
        # WiFi
        self._wifi = PipLabel(self, self._config, text="WiFi")
        self._wifi.pack(side="right")
        # Bluetooth
        self._bluetooth = PipLabel(self, self._config, text="BT")
        self._bluetooth.pack(side="right")
        self.pack(side=RIGHT)
