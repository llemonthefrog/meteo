import sys
import time

class Logger:
    def __init__(self, name="app", level="INFO"):
        self.name = name
        self.level = level

    def _log(self, level, msg):
        now = time.ticks_ms() // 1000
        print(f"[{now:5}s] [{self.name}] {level}: {msg}", file=sys.stdout)

    def info(self, msg): 
        if self.level in ("INFO", "DEBUG"):
            self._log("INFO", msg)

    def error(self, msg): 
        self._log("ERROR", msg)

    def debug(self, msg): 
        if self.level == "DEBUG":
            self._log("DEBUG", msg)

logger = Logger(level="DEBUG")
