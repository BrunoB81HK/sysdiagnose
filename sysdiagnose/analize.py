import argparse

from . import config


logger = config.logger.getChild(__name__)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "analyse",
        help="Analyse the results produced by parsers.",
    )
    parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=["a", "b"],
        help="the case to analyse",
    )
    parser.add_argument(
        "analizer",
        type=str,
        nargs="+",
        choices=["all", ""],
        help="the analizer(s) to use",
    )
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    return 0


"""
import config
import parsing

import os
import sys
import glob
import importlib.util
from docopt import docopt
from tabulate import tabulate

version_string = "analyse.py v2023-04-27 Version 1.0"





def analyse(analyser, caseid):
    # Load parser module
    spec = importlib.util.spec_from_file_location(
        analyser[:-3], config.analysers_folder + "/" + analyser + ".py"
    )
    print(spec, file=sys.stderr)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # building command
    parse_data_path = "%s/%s/" % (config.parsed_data_folder, caseid)
    output_file = (
        config.parsed_data_folder
        + caseid
        + "/"
        + analyser
        + "."
        + module.analyser_format
    )
    command = "module.%s('%s', '%s')" % (
        module.analyser_call,
        parse_data_path,
        output_file,
    )
    result = eval(command)

    print(f"Execution success, output saved in: {output_file}", file=sys.stderr)

    return 0


def allanalysers(caseid):
    os.chdir(config.analysers_folder)
    modules = glob.glob(os.path.join(os.path.dirname("."), "*.py"))
    os.chdir("..")
    for analyser in modules:
        try:
            print(f"Trying: {analyser[:-3]}", file=sys.stderr)
            analyse(analyser[:-3], caseid)
        except:  # noqa: E722
            continue
    return 0


# --------------------------------------------------------------------------- #


def main():
    if sys.version_info[0] < 3:
        print("Must be using Python 3! Exiting ...", file=sys.stderr)
        sys.exit(-1)

    arguments = docopt(__doc__, version=version_string)
    if arguments["list"] and arguments["cases"]:
        parsing.list_cases(config.cases_file)
    elif arguments["list"] and arguments["analysers"]:
        list_analysers(config.analysers_folder)
    elif arguments["analyse"]:
        if arguments["<case_number>"].isdigit():
            analyse(arguments["<analyser>"], arguments["<case_number>"])
        else:
            print("case number should be ... a number ...", file=sys.stderr)
    elif arguments["allanalysers"]:
        if arguments["<case_number>"].isdigit():
            allanalysers(arguments["<case_number>"])
        else:
            print("case number should be ... a number ...", file=sys.stderr)

    print(f"Running {version_string}\n", file=sys.stderr)
    return

    """
