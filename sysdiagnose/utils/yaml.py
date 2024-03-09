import pathlib

import yaml


__all__ = ("load", "dump")


# === Loader === #
def __path_constructor(loader: yaml.Loader, node: yaml.ScalarNode):
    return pathlib.Path(loader.construct_scalar(node))


yaml.SafeLoader.add_constructor("!path", __path_constructor)


# === Dumper === #
def __path_representer(dumper: yaml.Dumper, data: pathlib.Path) -> yaml.ScalarNode:
    return dumper.represent_scalar("!path", data.absolute().as_posix())


yaml.SafeDumper.add_representer(pathlib.PosixPath, __path_representer)


# === Functions === #
def load(file: pathlib.Path) -> dict:
    return yaml.safe_load(file.read_text())


def dump(data: dict, file: pathlib.Path) -> None:
    file.write_text(yaml.safe_dump(data))
