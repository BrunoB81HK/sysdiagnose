import argparse

import tabulate
import yaml

from . import config


logger = config.logger.getChild("list")


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "list",
        help="List the cases, parsers or analizers of the project.",
    )
    parser.add_argument(
        "item",
        type=str,
        choices=[
            "cases",
            "parsers",
            "analysers",
        ],
        help="the item to list",
    )
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    if args.item == "cases":
        return list_cases()
    elif args.item == "parsers":
        return list_parsers()
    elif args.item == "analysers":
        return list_analysers()

    logger.error(f"'{args.item:s}' is not a valid item to list. {{ cases | parsers | analysers }}")
    return 1


def list_cases() -> int:
    headers = ("ID", "Source file", "SHA256")

    cases = yaml.safe_load(config.cases_file.read_text())["cases"]
    lines = [(case_id, case_info["source_file"], case_info["source_sha256"]) for case_id, case_info in cases.items()]

    print(tabulate.tabulate(lines, headers=headers))
    return 0


def list_parsers() -> int:
    headers = ("Name", "Description", "Input")
    lines = []

    # from . import parsers
    #
    # lines = [parser for parser in parsers.__all__]
    #
    # os.chdir(folder)
    # modules = glob.glob(os.path.join(os.path.dirname("."), "*.py"))
    # lines = []
    # for parser in modules:
    #    try:
    #        spec = importlib.util.spec_from_file_location(parser[:-3], parser)
    #        module = importlib.util.module_from_spec(spec)
    #        spec.loader.exec_module(module)
    #        line = [parser[:-3], module.parser_description, module.parser_input]
    #        lines.append(line)
    #    except:  # noqa: E722
    #        continue

    print(tabulate.tabulate(lines, headers=headers))
    return 0


def list_analysers() -> int:
    headers = ("Name", "Description")
    lines = []

    # os.chdir(folder)
    # modules = glob.glob(os.path.join(os.path.dirname("."), "*.py"))
    # lines = []
    # for analyser in modules:
    #    try:
    #        spec = importlib.util.spec_from_file_location(analyser[:-3], analyser)
    #        module = importlib.util.module_from_spec(spec)
    #        spec.loader.exec_module(module)
    #        line = [analyser[:-3], module.analyser_description]
    #        lines.append(line)
    #    except:  # noqa: E722
    #        continue

    print(tabulate.tabulate(lines, headers=headers))
    return 0
