from datetime import datetime
from tkinter import LEFT, BOTTOM, RIGHT, BOTH, Y, END

from requests import get

from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipListbox import PipListbox
from PipHome.PipLog import Logger
from PipHome.PipSchedule import GLOBAL_SCHEDULER, MINUTE, SECOND, HOUR
from PipHome.PipTab import PipTab


class TimeTab(PipTab):
    _logger = Logger("Tabs.TimeTab")

    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        self._paused = False
        self.notebook.add(self, text="Time")
        self._main_frame = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content, self._config)
        self._build_time(self._main_frame)
        self._build_date(self._main_frame)
        self._main_frame.pack(fill=BOTH, expand=1)
        return self._main_frame

    def _build_time(self, parent_content):
        font = "RobotoMono 48"
        time_frame = PipFrame(parent_content, self._config)
        center_frame = PipFrame(time_frame, self._config)
        self._hours = PipLabel(center_frame, self._config, text="xx", font=font)
        self._separator = PipLabel(center_frame, self._config, text=":", font=font)
        self._minutes = PipLabel(center_frame, self._config, text="xx", font=font)
        self._hours.pack(side=LEFT)
        self._separator.pack(side=LEFT)
        self._minutes.pack(side=LEFT)
        center_frame.pack(fill=Y, expand=1)
        time_frame.pack(fill=BOTH, expand=1)
        GLOBAL_SCHEDULER.add_task("update clock", self._update_time)
        GLOBAL_SCHEDULER.add_task("update clock separator", self._update_time_separator)

    def _build_date(self, parent_content):
        font = "RobotoMono 18"
        self._date_frame = PipFrame(parent_content, self._config)
        self._date = PipLabel(self._date_frame, self._config, text="...", font=font)
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
        now = datetime.now().strftime(self._config["gui.time_tab.date_format"])
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

    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        notebook.add(self, text="Home")
        self._main_frame = None
        self._home = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content, self._config)
        self._home = PipLabel(self._main_frame, self._config, text="Home label")
        self._home.pack()
        self._main_frame.pack(fill=BOTH, expand=1)
        return self._main_frame


class MiscTab(PipTab):
    _logger = Logger("Tabs.MiscTab")
    _main_frame = None
    _connection_properties = {
        "connection": "N/A",
        "ip": "N/A"
    }

    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        notebook.add(self, text="Misc")
        self._left_frame = None
        self._right_frame = None

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content, self._config)
        self._main_frame.pack(fill=BOTH, expand=True)
        self._main_frame.grid_columnconfigure(0, weight=1)
        self._main_frame.grid_columnconfigure(1, weight=3)
        self._main_frame.grid_rowconfigure(0, weight=1)
        self._build_left_frame(self._main_frame)
        self._build_connection_tab()
        return self._main_frame

    def _build_left_frame(self, parent_content):
        self._left_frame = PipFrame(parent_content, self._config)
        self._left_frame.grid(row=0, column=0, sticky="nsew")
        self._list = PipListbox(self._left_frame, self._config)
        self._list.bind('<<ListboxSelect>>', self._on_select)
        self._list.pack(side=LEFT, fill=BOTH, expand=True)
        self._list.insert(END, "Connection")
        self._list.insert(END, "System")
        self._list.select_set(0)

    def _build_right_frame(self, parent_content):
        if self._right_frame is not None:
            self._right_frame.pack_forget()
        self._right_frame = PipFrame(parent_content, self._config)
        self._right_frame.grid(row=0, column=1, sticky="nsew")

    def _on_select(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self._logger.info('You selected item %d: "%s"' % (index, value))
        if index == 0:
            self._build_connection_tab()
        elif index == 1:
            self._build_system_tab()
        else:
            self._logger.warn(f"Do not know what to render on selection {index}")
            self._build_connection_tab()

    def _build_connection_tab(self):
        self._logger.debug("Building `Connection` tab")
        self._build_right_frame(self._main_frame)
        row = 0
        connection_label = PipLabel(self._right_frame, self._config, text="Connection")
        connection_label.grid(row=row, column=0)
        self._connection_value_label = PipLabel(self._right_frame,
                                                self._config,
                                                text=self._connection_properties["connection"])
        self._connection_value_label.grid(row=row, column=1)
        row = row + 1
        ip_label = PipLabel(self._right_frame, self._config, text="IP")
        ip_label.grid(row=row, column=0)
        self._ip_value_label = PipLabel(self._right_frame, self._config, text=self._connection_properties["ip"])
        self._ip_value_label.grid(row=row, column=1)
        row = row + 1
        GLOBAL_SCHEDULER.add_task_if_not_present("ip check", self._load_ip)

    def _load_ip(self):
        try:
            self._logger.debug("Checking IP address")
            ip = get('https://api.ipify.org').text
            self._set_connection("Active")
            self._set_ip(ip)
        except Exception as e:
            self._logger.error(f"Cannot get IP! {e}")
            self._set_connection("Unavailable")
            self._set_ip("N/A")
        return HOUR

    def _set_connection(self, value):
        self._connection_properties["connection"] = value
        self._connection_value_label.config(text=value)

    def _set_ip(self, value):
        self._connection_properties["ip"] = value
        self._ip_value_label.config(text=value)

    def _build_system_tab(self):
        self._logger.debug("Building `Connection` tab")
        self._build_right_frame(self._main_frame)
        label = PipLabel(self._right_frame, self._config, text="system")
        label.pack(side=LEFT, anchor="nw", expand=True)
