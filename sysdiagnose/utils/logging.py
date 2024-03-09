import inspect
import logging

from .paths import log_file

__all__ = ()

# === Main logger === #
__main_logger = logging.getLogger("sysdiagnose")
__main_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - [%(name)s]: %(message)s")

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
__main_logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
__main_logger.addHandler(console_handler)


# === Logger getter === #
def get_logger(suffix: str = None) -> logging.Logger:
    if suffix is None:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        suffix = module.__file__

    return __main_logger.getChild(suffix)
