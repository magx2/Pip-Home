from datetime import datetime

import psutil
from requests import get

from PipHome.PipLog import Logger
from PipHome.PipSchedule import HOUR, SECOND, ONCE
from PipHome.PipUtils import format_bytes


class PipSystemInfo:
    _logger = Logger("PipSystemInfo")
    _system_info = {}

    def __init__(self, scheduler, config):
        self._scheduler = scheduler
        self._config = config

    def __getitem__(self, item):
        if item in self._system_info:
            return self._system_info[item]
        else:
            return "N/A"

    def start(self):
        self._schedule_task("ip check", self._load_ip, HOUR)
        self._schedule_task("CPU %", self._load_cpu_percent, SECOND * 10)
        self._schedule_task("CPU logical cores", self._load_cpu_cores, ONCE)
        self._schedule_task("CPU load avg", self._load_cpu_load_avg, SECOND * 10)
        self._schedule_task("Memory info", self._load_mem, SECOND * 10)
        self._schedule_task("Disk info", self._load_disk, SECOND * 10)

    def stop(self):
        self._scheduler.remove_tasks_with_group("PipSystemInfo")

    def _schedule_task(self, task_name, function, time):
        self._scheduler.add_task(task_name, self._build_task(task_name, function, time), group="PipSystemInfo")

    def _build_task(self, task_name, function, time):
        try:
            function()
        except Exception as e:
            self._logger.error(f"Task `{task_name}` failed with exception {e}")
        return time

    def _load_ip(self):
        self._logger.debug("Checking IP address")
        ip = get('https://api.ipify.org').text
        now = datetime.now().strftime("%H:%M:%S")
        self._system_info["connection"] = f"Active ({now})"
        self._system_info["ip"] = ip

    def _load_cpu_percent(self):
        self._logger.debug("Checking CPU percent")
        cpu_percent = round(psutil.cpu_percent(), 2)
        self._system_info["cpu_percent"] = str(cpu_percent) + "%"

    def _load_cpu_cores(self):
        self._logger.debug("Checking CPU cores")
        cpu_cores = round(psutil.cpu_count(), 2)
        self._system_info["cpu_cores"] = str(cpu_cores)

    def _load_cpu_load_avg(self):
        self._logger.debug("Checking CPU load avg")
        cpu_load_avg = ", ".join(
            map(str,
                map(lambda x: round(x, 2),
                    psutil.getloadavg())))
        self._system_info["cpu_load_avg"] = str(cpu_load_avg)

    def _load_mem(self):
        self._logger.debug("Checking Memory")
        memory = psutil.virtual_memory()
        self._system_info["mem_total"] = format_bytes(memory.total)
        self._system_info["mem_used"] = format_bytes(memory.used)
        self._system_info["mem_free"] = format_bytes(memory.total - memory.used)

    def _load_disk(self):
        path = self._config["system.disk_check_path"]
        self._logger.debug(f"Checking Disk for path `{path}`")
        disk = psutil.disk_usage(path)
        self._system_info["disk_total"] = format_bytes(disk.total)
        self._system_info["disk_used"] = format_bytes(disk.used)
        self._system_info["disk_free"] = format_bytes(disk.free)
