"""
Module with functions to handle yaml files.
"""

import pathlib

import semver.version
import yaml


__all__ = ("load", "dump")


# === Loader === #
def __path_constructor(loader: yaml.Loader, node: yaml.ScalarNode) -> pathlib.Path:
    return pathlib.Path(loader.construct_scalar(node))


def __version_constructor(loader: yaml.Loader, node: yaml.ScalarNode) -> semver.version.Version:
    return semver.version.Version.parse(loader.construct_scalar(node))


yaml.SafeLoader.add_constructor("!path", __path_constructor)
yaml.SafeLoader.add_constructor("!version", __version_constructor)


# === Dumper === #
def __path_representer(dumper: yaml.Dumper, data: pathlib.Path) -> yaml.ScalarNode:
    return dumper.represent_scalar("!path", data.absolute().as_posix())


def __version_representer(dumper: yaml.Dumper, data: semver.version.Version) -> yaml.ScalarNode:
    return dumper.represent_scalar("!version", str(data))


yaml.SafeDumper.add_representer(pathlib.PosixPath, __path_representer)
yaml.SafeDumper.add_representer(semver.version.Version, __version_representer)


# === Functions === #
def loads(data: str) -> dict:
    return yaml.safe_load(data)


def load(file: pathlib.Path) -> dict:
    return loads(file.read_text())


def dumps(data: dict) -> str:
    return yaml.safe_dump(data)


def dump(data: dict, file: pathlib.Path) -> None:
    file.write_text(dumps(data))
