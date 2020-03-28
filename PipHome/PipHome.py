from tkinter import *
from tkinter import ttk

from PipHome.PipLog import Logger
from PipHome.PipNotebook import PipNotebook
from PipHome.PipSchedule import GLOBAL_SCHEDULER
from PipHome.PipStatusBar import PipStatusBar
from PipHome.Tabs import TimeTab, HomeTab

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

    _configure_style(gui_config)

    # tabs
    tabs = PipNotebook(root)
    tabs.config(padding="0")
    TimeTab(tabs, time_tab_config=gui_config["time_tab"])
    HomeTab(tabs)
    tabs.pack(expand=1, fill="both")

    # bottom frame
    PipStatusBar(root, borderwidth="0")

    root.mainloop()


def _configure_style(gui_config):
    # style https://stackoverflow.com/questions/23038356/change-color-of-tab-header-in-ttk-notebook/25444652
    style = ttk.Style()
    style.theme_create("pip_home", parent="alt", settings={
        "TFrame": {
            "configure": {
                "background": gui_config["label"]["background"],
            }
        },
        "TLabel": {
            "configure": {
                "background": gui_config["label"]["background"],
                "foreground": gui_config["label"]["foreground"],
                "font": "RobotoMono"
            }
        },
        "TNotebook": {
            "configure": {
                "tabmargins": [10, 10, 10, 0],
                "borderwidth": 0,
                "highlightthickness": 0,
                "background": gui_config["background"]
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [5, 5, 5, 0],
                "background": gui_config["label"]["background"],
                "foreground": gui_config["label"]["foreground"],
                "font": "RobotoMono 24"
            },
            "map": {
                "background": [("selected", gui_config["selected_tab"]["background"])],
                "foreground": [("selected", gui_config["selected_tab"]["foreground"])]
            }
        }
    })

    style.theme_use("pip_home")
