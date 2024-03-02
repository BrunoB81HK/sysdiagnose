"""
This file contains all of the configuration values for the project.
"""

import logging
import pathlib

import yaml

__all__ = (
    "data_path",
    "parsed_data_path",
    "app_config_path",
    "cases_file",
    "logger",
)

# === Parameters === #
debug = True

# == Paths === #
app_config_path = pathlib.Path.home() / ".local" / "share" / "sysdiagnose"
data_path = app_config_path / "data"
parsed_data_path = app_config_path / "parsed_data"
log_file = app_config_path / "app.log"
cases_file = app_config_path / "cases.yaml"

# Initialize the cases file.
app_config_path.mkdir(parents=True, exist_ok=True)
data_path.mkdir(parents=True, exist_ok=True)
parsed_data_path.mkdir(parents=True, exist_ok=True)
log_file.touch(exist_ok=True)
if not cases_file.exists():
    cases_file.write_text("cases: {}")

# === Loggers === #
logger = logging.getLogger("sysdiagnose")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s] - [%(levelname)s] - [%(name)s]: %(message)s"
)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# === YAML === #
def path_representer(dumper: yaml.Dumper, data: pathlib.Path) -> yaml.ScalarNode:
    return dumper.represent_scalar("!path", data.absolute().as_posix())


def path_constructor(loader: yaml.Loader, node: yaml.ScalarNode):
    return pathlib.Path(loader.construct_scalar(node))


yaml.SafeDumper.add_representer(pathlib.PosixPath, path_representer)
yaml.SafeLoader.add_constructor("!path", path_constructor)