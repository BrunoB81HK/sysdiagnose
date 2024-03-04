import argparse
import json
import os
import sys
import importlib.util
import glob

import yaml

from . import config


logger = config.logger.getChild(__name__)


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

    # Load parser module.
    module = importlib.import_module(parser, "parsers")
    spec = importlib.util.spec_from_file_location(parser[:-3], config.parsers_folder + parser + ".py")
    print(spec, file=sys.stderr)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # building command
    if isinstance(case[module.parser_input], str):
        command = "module." + module.parser_call + "('" + case[module.parser_input] + "')"
    else:
        command = "module." + module.parser_call + "(" + str(case[module.parser_input]) + ")"

    # running the command, expecting JSON output
    # try:
    #    result = eval(command)
    # except Exception as e:
    #    print(f'Error trying to parse {case[module.parser_input]}: {str(e)}', file=sys.stderr)

    result = eval(command)

    # saving the parser output
    output_file = config.parsed_data_folder + case_id + "/" + parser + ".json"
    with open(output_file, "w") as data_file:
        data_file.write(json.dumps(result, indent=4))

    print(f"Execution success, output saved in: {output_file}", file=sys.stderr)

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
