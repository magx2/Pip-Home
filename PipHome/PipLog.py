from datetime import datetime


class Logger:
    _log_levels_map = {
        "TRACE": 0,
        "DEBUG": 1,
        "INFO": 2,
        "WARN": 3,
        "ERROR": 4
    }

    def __init__(self, name, **options):
        if bool(options):
            self._options = options
        else:
            self._options = {"level": "DEBUG"}
        self._name = name

    def _log(self, level, msg, *values):
        if self._log_levels_map[level] >= self._log_levels_map[self._options["level"]]:
            if not type(msg) == str:
                msg = str(msg)
            print(str(datetime.now()) + " [" + level + "] [" + self._name + "] " + msg.format(*values))

    def trace(self, msg, *values):
        self._log("TRACE", msg, *values)

    def debug(self, msg, *values):
        self._log("DEBUG", msg, *values)

    def info(self, msg, *values):
        self._log("INFO", msg, *values)

    def warn(self, msg, *values):
        self._log("WARN", msg, *values)

    def error(self, msg, *values):
        self._log("ERROR", msg, *values)
