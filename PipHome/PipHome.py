from tkinter import *

from PipHome.PipConfig import PipConfig
from PipHome.PipLog import Logger
from PipHome.PipNotebook import PipNotebook
from PipHome.PipSchedule import GLOBAL_SCHEDULER
from PipHome.PipStatusBar import PipStatusBar
from PipHome.Tabs import TimeTab, HomeTab, MiscTab

_logger = Logger("PipHome", level="DEBUG")


def run(args):
    GLOBAL_SCHEDULER.start_main_loop()

    _render(PipConfig(args))


def _render(config):
    _logger.info("Starting application")
    # root
    root = Tk()
    root.geometry(str(config["gui.size.width"]) + "x" + str(config["gui.size.height"]))
    if config["gui"]["headless"]:
        root.overrideredirect(1)
    root.configure(background=config["gui.background"],
                   borderwidth="0",
                   highlightthickness="0")

    # tabs
    tabs = PipNotebook(root, config)
    TimeTab(tabs, config)
    HomeTab(tabs, config)
    MiscTab(tabs, config)
    tabs.pack(expand=1, fill="both")

    # bottom frame
    PipStatusBar(root, config, borderwidth="0")

    root.mainloop()
