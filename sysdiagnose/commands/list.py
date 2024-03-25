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
    parser.add_argument(
        "-n",
        "--names",
        action="store_true",
        help="list only the names",
    )

    parser.set_defaults(func=main)

    return parser


def main(args: argparse.Namespace) -> int:
    # Import the related modules.
    import tabulate

    from sysdiagnose.utils import logging

    # Get the logger.
    logger = logging.get_logger()

    # Set the item_function_mapping
    item_function_mapping = {
        "analyzers": list_analyzers,
        "cases": list_cases,
        "parsers": list_parsers,
    }

    if args.item not in item_function_mapping:
        logger.error(f"'{args.item:s}' is not a valid item to list. {{ analyzers | cases | parsers }}")
        return 1

    headers, lines, names = item_function_mapping[args.item]()

    if args.names:
        print("\n".join(names))
    else:
        print(tabulate.tabulate(lines, headers=headers))

    return 0


def list_analyzers() -> tuple[tuple[str, ...], tuple[str, ...], list[str]]:
    from sysdiagnose.utils import info

    headers = ("Name", "Version", "Description")
    lines = [
        (analyzer, analyzer_info["version"], analyzer_info["descritpion"])
        for analyzer, analyzer_info in info.get_all_analyzers().items()
    ]

    return headers, lines, info.all_analyzers


def list_cases() -> tuple[tuple[str, ...], tuple[str, ...], list[str]]:
    from sysdiagnose.utils import info

    headers = ("ID", "Source file", "SHA256")
    lines = [(case_id, case_info["source_file"], case_info["source_sha256"]) for case_id, case_info in info.get_all_cases().items()]

    return headers, lines, info.all_cases


def list_parsers() -> tuple[tuple[str, ...], tuple[str, ...], list[str]]:
    from sysdiagnose.utils import info

    headers = ("Name", "Version", "Description", "Input")
    lines = [
        (parser, parser_info["version"], parser_info["description"], parser_info["input"])
        for parser, parser_info in info.get_all_parsers().items()
    ]

    return headers, lines, info.all_parsers
