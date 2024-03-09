import argparse
import importlib.util
import pathlib

from .. import __version__

__all__ = ("add_version_argument", "add_command_parsers")


def add_version_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-v", "--version", action="version", version=__version__)


def add_command_parsers(parser: argparse.ArgumentParser) -> None:
    commands_parsers = parser.add_subparsers(title="commands")

    command_module_path = pathlib.Path(__file__).parent

    for module_file in command_module_path.glob("[!_]*.py"):
        # Import the modules.
        spec = importlib.util.spec_from_file_location(module_file.name, module_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Add the parser.
        sub_parser = module.add_parser(commands_parsers)

        # Add the version argument.
        add_version_argument(sub_parser)
