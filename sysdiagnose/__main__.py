import argparse
import pathlib
import signal

from . import __version__

from .init import init_main
from .list import list_main
from .parse import parse_main
from .analize import analyse_main


def main() -> None:
    # Register main parser.
    main_parser = argparse.ArgumentParser(
        prog="sysdiagnose",
        description="Forensic toolkit for iOS sysdiagnose feature.",
    )
    main_parser.add_argument("-v", "--version", action="version", version=__version__)

    # Register command parsers.
    subparsers = main_parser.add_subparsers(title="commands")

    # Register the 'init' command.
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a sysdiagnose analysis.",
    )
    init_parser.add_argument(
        "file",
        metavar="SYSDIAGNOSE_FILE",
        type=pathlib.Path,
        help="the sysdiagnose archive file",
    )
    init_parser.add_argument(
        "-f", "--force", action="store_true", help="force the re-initialization"
    )
    init_parser.set_defaults(func=init_main)

    # Register the 'list' command.
    list_parser = subparsers.add_parser(
        "list",
        help="List the cases, parsers or analizers of the project.",
    )
    list_parser.add_argument(
        "item",
        type=str,
        choices=[
            "cases",
            "parsers",
            "analysers",
        ],
        help="the item to list",
    )
    list_parser.set_defaults(func=list_main)

    # Register the 'parse' command.
    parse_parser = subparsers.add_parser(
        "parse",
        help="Parse extracted sysdiagnose files.",
    )
    parse_parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=["a", "b"],
        help="the case to parse",
    )
    parse_parser.add_argument(
        "parser",
        type=str,
        nargs="+",
        choices=["all", ""],
        help="the parser(s) to use",
    )
    parse_parser.set_defaults(func=parse_main)

    # Register the 'analyse' command.
    analyse_parser = subparsers.add_parser(
        "analyse",
        help="Analyse the results produced by parsers.",
    )
    analyse_parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=["a", "b"],
        help="the case to analyse",
    )
    analyse_parser.add_argument(
        "analizer",
        type=str,
        nargs="+",
        choices=["all", ""],
        help="the analizer(s) to use",
    )
    analyse_parser.set_defaults(func=analyse_main)

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
