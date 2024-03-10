import inspect
import logging
import pathlib

from .paths import log_file

__all__ = ("get_logger",)


# === Main logger === #
class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in (logging.WARN, logging.ERROR):
            self._style._fmt = "[%(levelname)s] %(message)s"
        else:
            self._style._fmt = "%(message)s"
        return super().format(record)


__main_logger = logging.getLogger("sysdiagnose")
__main_logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - [%(name)s]: %(message)s")

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
__main_logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter())
__main_logger.addHandler(console_handler)


# === Logger getter === #
def get_logger(suffix: str = None) -> logging.Logger:
    if suffix is None:
        frame = inspect.stack()[1]
        suffix = pathlib.Path(frame.filename).stem

    return __main_logger.getChild(suffix)
