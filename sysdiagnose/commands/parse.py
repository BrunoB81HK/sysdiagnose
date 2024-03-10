import argparse

from sysdiagnose.utils import info


def parsers_completer(prefix: str, parsed_args: argparse.Namespace, **kwargs) -> list[str]:
    return [parser for parser in info.all_parsers if parser not in parsed_args.parser]


def add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "parse",
        help="Parse extracted sysdiagnose files.",
    )

    parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=info.all_cases,
        help="the case to parse",
    )

    parser_choice_group = parser.add_argument_group(
        "parsers choice options",
        "Options to choose the parser(s) to run. If none is provided, all parsers will be run.",
    ).add_mutually_exclusive_group()
    parser_choice_group.add_argument(
        "parsers",
        type=str,
        nargs="*",
        default=[],
        help="the parser(s) to run",
    ).completer = parsers_completer
    parser_choice_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="run all parsers",
    )

    parser.set_defaults(func=main)

    return parser


def main(args: argparse.Namespace) -> int:
    if args.all or not args.parsers:
        return parse(args.case_id)
    return parse(args.case_id, args.parsers)


def parse(case_id: str, parsers: list[str] = None) -> int:
    # Import the related modules.
    import importlib

    from sysdiagnose.utils import logging
    from sysdiagnose.utils import paths
    from sysdiagnose.utils import yaml

    # Get the logger.
    logger = logging.get_logger()

    logger.info(f"Processing case '{case_id:s}'...")

    if parsers is None:
        parsers = info.all_parsers

    # Check if the parsers are valid.
    invalid_parsers = [parser for parser in parsers if parser not in info.all_parsers]
    if invalid_parsers:
        logger.error(f"Invalid parser(s): [ {', '.join(invalid_parsers):s} ].")
        return 1

    # Open the cases file.
    cases = yaml.load(paths.cases_file)["cases"]

    # Load the case file.
    case_file = cases[case_id]["case_file"]
    case = yaml.load(case_file)

    for parser in parsers:
        logger.info(f"Running parser '{parser:s}'...")

        # Load the parser module.
        parser_module = importlib.import_module(f"sysdiagnose.parsers.{parser:s}")

        # Extract parser attributes.
        input_paths = case[parser_module.parser_input]
        if not isinstance(input_paths, list):
            input_paths = [input_paths]

        # Execute the parser.
        result = parser_module.main(*input_paths)

        if result is None:
            logger.error("Execution failed.")
            return 1

        # Saving the parser output.
        output_file = (paths.parsed_data_path / case_id / parser).with_suffix(".yaml")
        yaml.dump(result, output_file)

        logger.info(f"Execution success, output saved in: {output_file.as_posix():s}")

    return 0
