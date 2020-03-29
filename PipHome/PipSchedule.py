import threading
import time

from PipHome.PipLog import Logger

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

    def add_task(self, task_name, task_function):
        self._logger.debug(f"Adding task `{task_name}` to scheduler")
        self._tasks[task_name] = (task_function, 0)

    def add_task_if_not_present(self, task_name, task_function):
        if task_name not in self._tasks:
            self._tasks[task_name] = (task_function, 0)
        else:
            self._logger.debug(f"Not adding task `{task_name}`, because it's already exists")

    def _loop(self):
        while not self._stop:
            now = time.time()
            self._logger.trace("Running loop")
            tasks = self._tasks.copy()
            for task_name, value in tasks.items():
                (task, next_time_to_run) = value
                if now > next_time_to_run:
                    self._run(task_name, task, now)

    def _run(self, task_name, task, now):
        try:
            wait_for_next_execution_s = task()
            if wait_for_next_execution_s > 0:
                self._tasks[task_name] = (task, wait_for_next_execution_s + now)
            else:
                self._logger.info(f"Removing task `{task_name}`")
                del self._tasks[task_name]
        except Exception as err:
            self._logger.error("Got error while running task {}\n{}", task_name, err)


GLOBAL_SCHEDULER = Scheduler()
