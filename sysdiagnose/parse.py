import argparse
import os
import sys
import importlib
import glob

import yaml

from . import config
from . import utils


logger = config.logger.getChild("parse")


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "parse",
        help="Parse extracted sysdiagnose files.",
    )
    parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=utils.get_all_cases(),
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
    ).completer = utils.get_all_parsers
    parser_choice_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="run all parsers",
    )

    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    if args.all or not args.parsers:
        return parse(args.case_id)
    return parse(args.case_id, args.parsers)


def parse(case_id: str, parsers: list[str] = None) -> int:
    logger.info(f"Processing case '{case_id:s}'...")

    if parsers is None:
        parsers = utils.get_all_parsers()

    # Check if the parsers are valid.
    invalid_parsers = [parser for parser in parsers if parser not in utils.get_all_parsers()]
    if invalid_parsers:
        logger.error(f"Invalid parser(s): [ {', '.join(invalid_parsers):s} ].")
        return 1

    # Open the cases file.
    cases = yaml.safe_load(config.cases_file.read_text())["cases"]

    # Load the case file.
    case_file = cases[case_id]["case_file"]
    case = yaml.safe_load(case_file.read_text())

    for parser in parsers:
        logger.info(f"Running parser '{parser:s}'...")

        # Load parser module.
        parser_module = importlib.import_module(parser, "parsers")

        # Extract parser attributes.
        parser_call = getattr(parser_module, parser_module.parser_call)
        input_paths = case[parser_module.parser_input]
        if not isinstance(input_paths, list):
            input_paths = [input_paths]

        # Execute the parser.
        result = parser_call(*input_paths)

        # Saving the parser output.
        output_file = (config.parsed_data_path / case_id / parser).with_suffix(".yaml")
        output_file.write_text(yaml.safe_dump(result))

        logger.info(f"Execution success, output saved in: {output_file.as_posix():s}")

    return 0


def parse_all(case_id):
    # get list of working parsers
    # for each parser, run and save which is working
    # display list of successful parses
    os.chdir(config.parsers_folder)
    modules = glob.glob(os.path.join(os.path.dirname("."), "*.py"))
    os.chdir("..")
    for parser in modules:
        try:
            print(f"Trying: {parser[:-3]}", file=sys.stderr)
            parse(parser[:-3], case_id)
        except:  # noqa: E722
            continue
    return 0
