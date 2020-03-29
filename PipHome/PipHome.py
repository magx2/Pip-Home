from tkinter import *

from PipHome.PipConfig import PipConfig
from PipHome.PipLog import Logger
from PipHome.PipNotebook import PipNotebook
from PipHome.PipSchedule import GLOBAL_SCHEDULER
from PipHome.PipStatusBar import PipStatusBar
from PipHome.Tabs import TimeTab, HomeTab, MiscTab

_logger = Logger("PipHome", level="DEBUG")


def run(args):
    config = PipConfig(args)
    GLOBAL_SCHEDULER.start_main_loop()

    _render(config)


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
    tabs = PipNotebook(root)
    TimeTab(tabs, time_tab_config=config["gui.time_tab"])
    HomeTab(tabs)
    MiscTab(tabs)
    tabs.pack(expand=1, fill="both")

    # bottom frame
    PipStatusBar(root, borderwidth="0")

    root.mainloop()
