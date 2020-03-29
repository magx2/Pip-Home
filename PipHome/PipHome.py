from tkinter import *

from PipHome.PipLog import Logger
from PipHome.PipNotebook import PipNotebook
from PipHome.PipSchedule import GLOBAL_SCHEDULER
from PipHome.PipStatusBar import PipStatusBar
from PipHome.Tabs import TimeTab, HomeTab, MiscTab

_logger = Logger("PipHome", level="DEBUG")


def run(args):
    config = {
        "gui": {
            "headless": False,
            "size": {
                "width": 480,
                "height": 320
            },
            "background": "#0D0208",
            "label": {
                "foreground": "#008F11",
                "background": "#0D0208"
            },
            "selected_tab": {
                "foreground": "#0D0208",
                "background": "#008F11"
            },
            "time_tab": {
                # https://stackabuse.com/how-to-format-dates-in-python/
                "date_format": "%a, %d %b %Y"
            }
        }
    }
    GLOBAL_SCHEDULER.start_main_loop()

    _render(config["gui"])


def _render(gui_config):
    _logger.info("Starting application")
    # root
    root = Tk()
    size = gui_config["size"]
    root.geometry(str(size["width"]) + "x" + str(size["height"]))
    if gui_config["headless"]:
        root.overrideredirect(1)
    root.configure(background=gui_config["background"],
                   borderwidth="0",
                   highlightthickness="0")

    # tabs
    tabs = PipNotebook(root)
    TimeTab(tabs, time_tab_config=gui_config["time_tab"])
    HomeTab(tabs)
    MiscTab(tabs)
    tabs.pack(expand=1, fill="both")

    # bottom frame
    PipStatusBar(root, borderwidth="0")

    root.mainloop()
