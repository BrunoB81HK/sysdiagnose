import argparse
import signal

from . import __version__

from .init import add_parser as add_init_parser
from .list import add_parser as add_list_parser
from .parse import add_parser as add_parse_parser
from .analize import add_parser as add_analyse_parser


def main() -> None:
    # Register main parser.
    main_parser = argparse.ArgumentParser(
        prog="sysdiagnose",
        description="Forensic toolkit for iOS sysdiagnose feature.",
    )
    main_parser.add_argument("-v", "--version", action="version", version=__version__)

    # Register command parsers.
    subparsers = main_parser.add_subparsers(title="commands")
    add_init_parser(subparsers)
    add_list_parser(subparsers)
    add_parse_parser(subparsers)
    add_analyse_parser(subparsers)

    # Register the autocomplete.
    try:
        import argcomplete
    except ImportError:
        pass
    else:
        argcomplete.autocomplete(main_parser, exclude=["-h", "--help"])

    # Parse the command line arguments and call the sub command.
    args = main_parser.parse_args()

    try:
        ret_code = args.func(args)
    except KeyboardInterrupt:
        ret_code = signal.SIGINT
    except RuntimeError as e:
        ret_code = str(e)
    return ret_code
