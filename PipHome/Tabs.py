from datetime import datetime
from tkinter import LEFT, BOTTOM, RIGHT

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipLog import Logger
from PipHome.PipSchedule import GLOBAL_SCHEDULER, MINUTE, SECOND
from PipHome.PipTab import PipTab


class TimeTab(PipTab):
    _logger = Logger("Tabs.TimeTab")

    def __init__(self, notebook, time_tab_config, **kw):
        super().__init__(notebook, **kw)
        self._paused = False
        self._time_tab_config = time_tab_config
        self._build_time()
        self._build_date()
        self.notebook.add(self, text="Time")

    def _build_time(self):
        self._time_frame = PipFrame(self)
        self._hours = PipLabel(self._time_frame, text="xx")
        self._separator = PipLabel(self._time_frame, text=":")
        self._minutes = PipLabel(self._time_frame, text="xx")
        self._hours.pack(side=LEFT)
        self._separator.pack(side=LEFT)
        self._minutes.pack(side=LEFT)
        self._time_frame.pack()
        GLOBAL_SCHEDULER.add_task("update clock", self._update_time)
        GLOBAL_SCHEDULER.add_task("update clock separator", self._update_time_separator)

    def _build_date(self):
        self._date_frame = PipFrame(self)
        self._date = PipLabel(self._date_frame, text="...")
        self._date.pack(side=RIGHT)
        self._date_frame.pack(side=BOTTOM)
        GLOBAL_SCHEDULER.add_task("update date", self._update_date)

    def pause(self):
        self._paused = True

    def un_pause(self):
        self._paused = False

    def _update_time(self):
        self._logger.trace("Updating time")
        now = datetime.now()
        self._hours.config(text=str(_add_zero_if_missing(now.hour)))
        self._minutes.config(text=str(_add_zero_if_missing(now.minute)))
        return MINUTE

    def _update_date(self):
        self._logger.trace("Updating date")
        now = datetime.now().strftime(self._time_tab_config["date_format"])
        self._date.config(text=now)
        return MINUTE

    def _update_time_separator(self):
        self._logger.trace("Updating separator")
        text = self._separator.cget("text")
        if text == ":":
            self._separator.config(text=" ")
        else:
            self._separator.config(text=":")
        return SECOND


def _add_zero_if_missing(number):
    if number > 9:
        return str(number)
    else:
        return "0" + str(number)


class HomeTab(PipTab):
    _logger = Logger("Tabs.HomeTab")

    def __init__(self, notebook, **kw):
        super().__init__(notebook, **kw)
        self._home_tab = PipFrame(notebook, borderwidth="-2")
        notebook.add(self._home_tab, text="Home")
