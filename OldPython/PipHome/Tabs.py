from datetime import datetime
from tkinter import LEFT, BOTTOM, RIGHT, BOTH, Y, END, X

from PipHome.PipButton import PipButton
from PipHome.PipFrame import PipFrame
from PipHome.PipLabel import PipLabel
from PipHome.PipListbox import PipListbox
from PipHome.PipLog import Logger
from PipHome.PipSchedule import GLOBAL_SCHEDULER, MINUTE, SECOND
from PipHome.PipSystemInfo import PipSystemInfo
from PipHome.PipTab import PipTab


class TimeTab(PipTab):
    _logger = Logger("Tabs.TimeTab")

    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        self._paused = False
        self._main_frame = None
        self.notebook.add(self, text="Time")

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content, self._config)
        self._build_time(self._main_frame)
        self._build_date(self._main_frame)
        self._main_frame.pack(fill=BOTH, expand=1)

    def hide(self):
        self._main_frame.pack_forget()
        GLOBAL_SCHEDULER.remove_tasks_with_group("TimeTab")

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
        GLOBAL_SCHEDULER.add_task("update clock", self._update_time, group="TimeTab")
        GLOBAL_SCHEDULER.add_task("update clock separator", self._update_time_separator, group="TimeTab")

    def _build_date(self, parent_content):
        font = "RobotoMono 18"
        self._date_frame = PipFrame(parent_content, self._config)
        self._date = PipLabel(self._date_frame, self._config, text="...", font=font)
        self._date.pack(side=RIGHT)
        self._date_frame.pack(side=BOTTOM)
        GLOBAL_SCHEDULER.add_task("update date", self._update_date, group="TimeTab")

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

    def hide(self):
        self._main_frame.pack_forget()


class MiscTab(PipTab):
    _logger = Logger("Tabs.MiscTab")
    _main_frame = None

    def __init__(self, notebook, config, **kw):
        super().__init__(notebook, config, **kw)
        self._left_frame = None
        self._right_frame = None
        notebook.add(self, text="Misc")
        self._pip_system_info = PipSystemInfo(GLOBAL_SCHEDULER, config)

    def render(self, parent_content):
        self._main_frame = PipFrame(parent_content, self._config)
        self._main_frame.pack(fill=BOTH, expand=True)
        self._main_frame.grid_columnconfigure(0, weight=1)
        self._main_frame.grid_columnconfigure(1, weight=3)
        self._main_frame.grid_rowconfigure(0, weight=1)
        self._build_left_frame(self._main_frame)
        self._build_system_tab()
        self._pip_system_info.start()
        return self._main_frame

    def hide(self):
        self._main_frame.pack_forget()
        self._pip_system_info.stop()

    def _build_left_frame(self, parent_content):
        self._left_frame = PipFrame(parent_content, self._config)
        self._left_frame.grid(row=0, column=0, sticky="nsew")
        self._list = PipListbox(self._left_frame, self._config)
        self._list.bind('<<ListboxSelect>>', self._on_select)
        self._list.pack(side=LEFT, fill=BOTH, expand=True)
        self._list.insert(END, "System")
        self._list.insert(END, "Quit")
        self._list.select_set(0)

    def _build_right_frame(self, parent_content):
        if self._right_frame is not None:
            self._right_frame.pack_forget()
        self._right_frame = PipFrame(parent_content, self._config, padx=5, pady=5)
        self._right_frame.grid(row=0, column=1, sticky="nsew")

    def _on_select(self, event):
        w = event.widget
        if len(w.curselection()) > 0:
            index = int(w.curselection()[0])
        else:
            index = 0
        if index == 0:
            self._build_system_tab()
        elif index == 1:
            self._build_quit_tab()
        else:
            self._logger.warn(f"Do not know what to render on selection {index}")
            self._build_system_tab()

    def _build_system_tab(self):
        self._logger.debug("Building `Connection` tab")
        self._build_right_frame(self._main_frame)

        # Connection header
        row = 0
        PipLabel(self._right_frame, self._config, text="Internet Info").grid(row=row, column=0, columnspan=4)

        # Connection
        row = row + 1
        PipLabel(self._right_frame, self._config, text="Connection").grid(row=row, column=0)
        self._connection_value_label = PipLabel(self._right_frame,
                                                self._config,
                                                text=self._pip_system_info["connection"])
        self._connection_value_label.grid(row=row, column=1)

        # IP
        PipLabel(self._right_frame, self._config, text="IP").grid(row=row, column=2)
        self._ip_value_label = PipLabel(self._right_frame, self._config, text=self._pip_system_info["ip"])
        self._ip_value_label.grid(row=row, column=3)

        # CPU header
        row = row + 1
        PipLabel(self._right_frame, self._config, text="CPU Info").grid(row=row, column=0, columnspan=4)

        # cpu %
        row = row + 1
        PipLabel(self._right_frame, self._config, text="CPU %").grid(row=row, column=0)
        self._cpu_value_label = PipLabel(self._right_frame, self._config, text=self._pip_system_info["cpu_percent"])
        self._cpu_value_label.grid(row=row, column=1)

        # cpu cores
        # row = row + 1
        cpu_cores_label = PipLabel(self._right_frame, self._config, text="CPU cores")
        cpu_cores_label.grid(row=row, column=2)
        self._cpu_cores_value_label = PipLabel(self._right_frame, self._config, text=self._pip_system_info["cpu_cores"])
        self._cpu_cores_value_label.grid(row=row, column=3)

        # cpu load avg
        row = row + 1
        PipLabel(self._right_frame, self._config, text="CPU load avg 1, 5, 15 min").grid(row=row, column=0,
                                                                                         columnspan=2)
        self._cpu_load_avg_value_label = PipLabel(self._right_frame, self._config,
                                                  text=self._pip_system_info["cpu_load_avg"])
        self._cpu_load_avg_value_label.grid(row=row, column=2, columnspan=2)

        # Memory & disk header
        row = row + 1
        PipLabel(self._right_frame, self._config, text="Memory Info").grid(row=row, column=0, columnspan=2)
        PipLabel(self._right_frame, self._config, text="Disk Info").grid(row=row, column=2, columnspan=2)

        # Memory total
        row = row + 1
        PipLabel(self._right_frame, self._config, text="Total").grid(row=row, column=0)
        self._mem_total_value_label = PipLabel(self._right_frame, self._config,
                                               text=self._pip_system_info["mem_total"])
        self._mem_total_value_label.grid(row=row, column=1)

        # Disk total
        PipLabel(self._right_frame, self._config, text="Total").grid(row=row, column=2)
        self._disk_total_value_label = PipLabel(self._right_frame, self._config,
                                                text=self._pip_system_info["disk_total"])
        self._disk_total_value_label.grid(row=row, column=3)

        # Memory used
        row = row + 1
        PipLabel(self._right_frame, self._config, text="Used").grid(row=row, column=0)
        self._mem_used_value_label = PipLabel(self._right_frame, self._config,
                                              text=self._pip_system_info["mem_used"])
        self._mem_used_value_label.grid(row=row, column=1)

        # Disk used
        PipLabel(self._right_frame, self._config, text="Used").grid(row=row, column=2)
        self._disk_used_value_label = PipLabel(self._right_frame, self._config,
                                               text=self._pip_system_info["disk_used"])
        self._disk_used_value_label.grid(row=row, column=3)

        # Memory free
        row = row + 1
        PipLabel(self._right_frame, self._config, text="Free").grid(row=row, column=0)
        self._mem_free_value_label = PipLabel(self._right_frame, self._config,
                                              text=self._pip_system_info["mem_free"])
        self._mem_free_value_label.grid(row=row, column=1)

        # Disk free
        PipLabel(self._right_frame, self._config, text="Free").grid(row=row, column=2)
        self._disk_free_value_label = PipLabel(self._right_frame, self._config,
                                               text=self._pip_system_info["disk_free"])
        self._disk_free_value_label.grid(row=row, column=3)

        # Refresh button
        row = row + 1
        refresh = PipButton(self._right_frame, self._config, text="Refresh", command=self._build_system_tab)
        refresh.grid(row=row, column=0, columnspan=4, stick="we")

    def _build_quit_tab(self):
        self._logger.debug("Building `Connection` tab")
        self._build_right_frame(self._main_frame)
        restart = PipButton(self._right_frame, self._config, text="Restart")
        restart.pack(fill=X)
        shutdown = PipButton(self._right_frame, self._config, text="Shutdown")
        shutdown.pack(fill=X)
