import argparse
import signal

from . import commands


def main() -> None:
    # Register main parser.
    main_parser = argparse.ArgumentParser(
        prog="sysdiagnose",
        description="Forensic toolkit for iOS sysdiagnose feature.",
    )
    commands.add_version_argument(main_parser)

    # Register the commands parsers.
    commands.add_command_parsers(main_parser)

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


if __name__ == "__main__":
    import sys

    sys.exit(main())
