import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
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
            "analyzers",
        ],
        help="the item to list",
    )

    parser.set_defaults(func=main)

    return parser


def main(args: argparse.Namespace) -> int:
    # Import the related modules.
    from ..utils import logging

    # Get the logger.
    logger = logging.get_logger()

    if args.item == "cases":
        return list_cases()
    elif args.item == "parsers":
        return list_parsers()
    elif args.item == "analyzers":
        return list_analyzers()

    logger.error(f"'{args.item:s}' is not a valid item to list. {{ cases | parsers | analyzers }}")
    return 1


def list_cases() -> int:
    import tabulate

    from ..utils import paths
    from ..utils import yaml

    headers = ("ID", "Source file", "SHA256")

    cases = yaml.load(paths.cases_file)["cases"]
    lines = [(case_id, case_info["source_file"], case_info["source_sha256"]) for case_id, case_info in cases.items()]

    print(tabulate.tabulate(lines, headers=headers))
    return 0


def list_parsers() -> int:
    import tabulate

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


def list_analyzers() -> int:
    import tabulate

    headers = ("Name", "Description")
    lines = []

    # os.chdir(folder)
    # modules = glob.glob(os.path.join(os.path.dirname("."), "*.py"))
    # lines = []
    # for analyzer in modules:
    #    try:
    #        spec = importlib.util.spec_from_file_location(analyzer[:-3], analyzer)
    #        module = importlib.util.module_from_spec(spec)
    #        spec.loader.exec_module(module)
    #        line = [analyzer[:-3], module.analyzer_description]
    #        lines.append(line)
    #    except:  # noqa: E722
    #        continue

    print(tabulate.tabulate(lines, headers=headers))
    return 0
