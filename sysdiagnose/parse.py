import argparse
import os
import sys
import importlib.util
import glob

import yaml

from . import config


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
        choices=["a", "b"],
        help="the case to parse",
    )
    parser.add_argument(
        "parser",
        type=str,
        nargs="+",
        choices=["all", ""],
        help="the parser(s) to use",
    )
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    # TODO: Test if case_id and parser is valid
    return parse(args.parser, args.case_id)


def parse(parser: str, case_id: str) -> int:
    logger.info(f"Processing case '{case_id:s}'...")

    # Open the cases file.
    cases = yaml.safe_load(config.cases_file.read_text())["cases"]

    # Load the case file.
    case_file = cases[case_id]["case_file"]
    case = yaml.safe_load(case_file.read_text())

    if parser == "all":
        # TODO: Implement.
        return 0

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
