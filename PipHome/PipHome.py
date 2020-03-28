from tkinter import *
from tkinter import ttk

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipNotebook import PipNotebook


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
    render(config["gui"])


def render(gui_config):
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

    time_tab = PipFrame(tabs, borderwidth="-2")
    time = PipLabel(time_tab, text="17:22")
    time.pack()
    tabs.add(time_tab, text="Time")

    home_tab = PipFrame(tabs, borderwidth="-2")
    tabs.add(home_tab, text="Home")

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
