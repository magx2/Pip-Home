from inspect import getmembers, isfunction
from tkinter import *
from tkinter import ttk

from PipHome import Tabs
from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipLog import Logger
from PipHome.PipNotebook import PipNotebook
from PipHome.PipSchedule import GLOBAL_SCHEDULER

_logger = Logger("PipHome", level="DEBUG")

def run(args):
    config = {
        "gui": {
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
            }
        }
    }
    GLOBAL_SCHEDULER.start_main_loop()

    functions_list = list(
        filter(lambda func: func[0].startswith("render"),
               [o for o in getmembers(Tabs) if isfunction(o[1])]))
    _logger.debug("Found functions to render tabs: {}", ", ".join(list(map(lambda func: func[0], functions_list))))
    render(config["gui"], list(map(lambda func: func[1], functions_list)))


def render(gui_config, tabs_functions):
    _logger.info("Starting application")
    # root
    root = Tk()
    size = gui_config["size"]
    root.geometry(str(size["width"]) + "x" + str(size["height"]))
    root.overrideredirect(1)
    root.configure(background=gui_config["background"],
                   borderwidth="0",
                   highlightthickness="0")

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
                "foreground": gui_config["label"]["foreground"]
            }
        },
        "TNotebook": {
            "configure": {
                # "tabmargins": [2, 5, 2, 0],
                "borderwidth": 0,
                "highlightthickness": 0,
                "background": gui_config["background"]
            }
        },
        "TNotebook.Tab": {
            "configure": {
                # "padding": [5, 1],
                "background": gui_config["label"]["background"],
                "foreground": gui_config["label"]["foreground"]
            },
            "map": {
                "background": [("selected", gui_config["selected_tab"]["background"])],
                "foreground": [("selected", gui_config["selected_tab"]["foreground"])]
                # ,"expand": [("selected", [1, 1, 1, 0])]
            }
        }
    })

    style.theme_use("pip_home")

    # tabs
    tabs = PipNotebook(root)
    tabs.config(padding="0")
    for tab_function in tabs_functions:
        tab_function(tabs)
    tabs.pack(expand=1, fill="both")

    # bottom frame
    bottom_frame = PipFrame(root, borderwidth="0")
    bottom_frame.pack(side=RIGHT)
    battery = PipLabel(bottom_frame, text="100%")
    battery.pack(side="right")
    wifi = PipLabel(bottom_frame, text="WiFi")
    wifi.pack(side="right")
    bluetooth = PipLabel(bottom_frame, text="BT")
    bluetooth.pack(side="right")

    root.mainloop()
