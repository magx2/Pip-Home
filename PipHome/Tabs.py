from datetime import datetime
from tkinter import LEFT, BOTTOM, RIGHT, BOTH, Y, TOP, END

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipListbox import PipListbox
from PipHome.PipLog import Logger
from PipHome.PipSchedule import GLOBAL_SCHEDULER, MINUTE, SECOND
from PipHome.PipTab import PipTab


class TimeTab(PipTab):
    _logger = Logger("Tabs.TimeTab")

    def __init__(self, notebook, time_tab_config, **kw):
        super().__init__(notebook, **kw)
        self._paused = False
        self._time_tab_config = time_tab_config
        self.notebook.add(self, text="Time")
        self._main_frame = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content)
        self._build_time(self._main_frame)
        self._build_date(self._main_frame)
        self._main_frame.pack(fill=BOTH, expand=1)
        return self._main_frame

    def _build_time(self, parent_content):
        font = "RobotoMono 48"
        time_frame = PipFrame(parent_content)
        center_frame = PipFrame(time_frame)
        self._hours = PipLabel(center_frame, text="xx", font=font)
        self._separator = PipLabel(center_frame, text=":", font=font)
        self._minutes = PipLabel(center_frame, text="xx", font=font)
        self._hours.pack(side=LEFT)
        self._separator.pack(side=LEFT)
        self._minutes.pack(side=LEFT)
        center_frame.pack(fill=Y, expand=1)
        time_frame.pack(fill=BOTH, expand=1)
        GLOBAL_SCHEDULER.add_task("update clock", self._update_time)
        GLOBAL_SCHEDULER.add_task("update clock separator", self._update_time_separator)

    def _build_date(self, parent_content):
        font = "RobotoMono 18"
        self._date_frame = PipFrame(parent_content)
        self._date = PipLabel(self._date_frame, text="...", font=font)
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
        notebook.add(self, text="Home")
        self._main_frame = None
        self._home = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content)
        self._home = PipLabel(self._main_frame, text="Home label")
        self._home.pack()
        self._main_frame.pack(fill=BOTH, expand=1)
        return self._main_frame


class MiscTab(PipTab):
    _logger = Logger("Tabs.MiscTab")

    def __init__(self, notebook, **kw):
        super().__init__(notebook, **kw)
        notebook.add(self, text="Misc")
        self._main_frame = None
        self._left_frame = None
        self._right_frame = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content)
        self._build_left_frame(self._main_frame)
        self._right_frame = PipFrame(self._main_frame)
        self._right_frame.pack(fill=Y, expand=1, side=RIGHT)
        self._main_frame.pack(fill=BOTH, expand=1)
        return self._main_frame

    def _build_left_frame(self, parent_content):
        self._left_frame = PipFrame(parent_content)
        self._left_frame.pack(fill=Y, expand=1, side=LEFT)
        self._list = PipListbox(parent_content)
        self._list.pack(side=TOP)
        self._list.insert(END, "Connection")
        self._list.insert(END, "System")
