from datetime import datetime
from tkinter import LEFT

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipLog import Logger
from PipHome.PipSchedule import GLOBAL_SCHEDULER, MINUTE, SECOND

_update_time_logger = Logger("Tabs.update_time")


def render_01_time_tab(root_notebook):
    time_tab = PipFrame(root_notebook, borderwidth="-2")
    time_frame = PipFrame(time_tab)
    hours = PipLabel(time_frame, text="17")
    separator = PipLabel(time_frame, text=":")
    minutes = PipLabel(time_frame, text="22")
    hours.pack(side=LEFT)
    separator.pack(side=LEFT)
    minutes.pack(side=LEFT)
    time_frame.pack()
    root_notebook.add(time_tab, text="Time")
    GLOBAL_SCHEDULER.add_task("update clock", lambda: _update_time(hours, minutes))
    GLOBAL_SCHEDULER.add_task("update clock separator", lambda: _update_time_separator(separator))


def _update_time(hours, minutes):
    _update_time_logger.trace("Updating time")
    now = datetime.now()
    hours.config(text=str(_add_zero_if_missing(now.hour)))
    minutes.config(text=str(_add_zero_if_missing(now.minute)))
    return MINUTE


def _update_time_separator(separator):
    text = separator.cget("text")
    if text == ":":
        separator.config(text=" ")
    else:
        separator.config(text=":")
    return SECOND


def _add_zero_if_missing(number):
    if number > 9:
        return str(number)
    else:
        return "0" + str(number)


def render_02_home_tab(root_notebook):
    home_tab = PipFrame(root_notebook, borderwidth="-2")
    root_notebook.add(home_tab, text="Home")
