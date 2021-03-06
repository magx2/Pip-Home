import threading
import time

from PipHome.PipLog import Logger

ONCE = -1
SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60


class Scheduler:
    _logger = Logger("Scheduler")
    _main_loop_thread = None

    def __init__(self):
        self._main_loop_thread = threading.Thread(target=self._loop, daemon=True)
        self._tasks = {}
        self._stop = True

    def start_main_loop(self):
        self._logger.info("Starting main loop")
        if not self._stop:
            raise Exception("This scheduler is already running!")
        self._stop = False
        self._main_loop_thread.start()

    def stop_main_loop(self):
        if self._stop:
            raise Exception("This scheduler is already stopped!")
        self._stop = True

    def add_task(self, task_name, task_function, **options):
        if "group" in options:
            task_name = options["group"] + "." + task_name
        if task_name not in self._tasks:
            self._logger.debug(f"Adding task `{task_name}` to scheduler")
            self._tasks[task_name] = (task_function, 0)
        else:
            self._logger.debug(f"Not adding task `{task_name}`, because it's already exists")

    def remove_tasks_with_group(self, group):
        tasks = self._tasks.copy()
        new_tasks = {}
        for k in tasks.keys():
            if not k.startswith(group + "."):
                new_tasks[k] = tasks[k]
            else:
                self._logger.debug(f"Removing task `{k}` because it is in group `{group}`")
        self._tasks = new_tasks

    def _loop(self):
        while not self._stop:
            now = time.time()
            self._logger.trace(f"Running loop, number of tasks {len(self._tasks)}")
            tasks = self._tasks.copy()
            for task_name, value in tasks.items():
                (task, next_time_to_run) = value
                if now > next_time_to_run:
                    self._run(task_name, task, now)

    def _run(self, task_name, task, now):
        try:
            wait_for_next_execution_s = task()
            if wait_for_next_execution_s is not None and wait_for_next_execution_s > 0:
                self._tasks[task_name] = (task, wait_for_next_execution_s + now)
            else:
                self._logger.debug(f"Task `{task_name}` do not want to be run again")
                del self._tasks[task_name]
        except Exception as err:
            self._logger.error("Got error while running task {}\n{}", task_name, err)


GLOBAL_SCHEDULER = Scheduler()
