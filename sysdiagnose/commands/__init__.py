import argparse

__all__ = ("add_version_argument", "add_command_parsers")


def add_version_argument(parser: argparse.ArgumentParser) -> None:
    from .. import __version__

    parser.add_argument("-v", "--version", action="version", version=__version__)


def add_command_parsers(parser: argparse.ArgumentParser) -> None:
    import importlib
    import pathlib

    commands_parsers = parser.add_subparsers(title="commands")

    command_module_path = pathlib.Path(__file__).parent

    for module_file in command_module_path.glob("[!_]*.py"):
        # Import the modules.
        module = importlib.import_module(f"sysdiagnose.commands.{module_file.stem:s}")

        # Add the parser.
        sub_parser = module.add_parser(commands_parsers)

        # Add the version argument.
        add_version_argument(sub_parser)
