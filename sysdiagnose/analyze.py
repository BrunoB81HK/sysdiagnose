import argparse
import importlib

from . import config
from . import utils


logger = config.logger.getChild("analyze")


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "analyze",
        help="Analyze the results produced by parsers.",
    )
    parser.add_argument(
        "case_id",
        metavar="ID",
        type=str,
        choices=["a", "b"],
        help="the case to analyze",
    )

    analyzer_choice_group = parser.add_argument_group(
        "analyzers choice options",
        "Options to choose the analyzer(s) to run. If none is provided, all analyzers will be run.",
    ).add_mutually_exclusive_group()
    analyzer_choice_group.add_argument(
        "analyzers",
        type=str,
        nargs="*",
        default=[],
        help="the analyzer(s) to run",
    ).completer = utils.get_all_analyzers
    analyzer_choice_group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="run all parsers",
    )

    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    if args.all or not args.analyzers:
        return analyze(args.case_id)
    return analyze(args.case_id, args.analyzers)


def analyze(case_id: str, analyzers: list[str] = None) -> int:
    logger.info(f"Processing case '{case_id:s}'...")

    if analyzers is None:
        analyzers = utils.get_all_analyzers()

    # Check if the analyzers are valid.
    invalid_analyzers = [analyzer for analyzer in analyzers if analyzer not in utils.get_all_analyzers()]
    if invalid_analyzers:
        logger.error(f"Invalid analyzer(s): [ {', '.join(invalid_analyzers):s} ].")
        return 1

    for analyzer in analyzers:
        logger.info(f"Running analyzer '{analyzer:s}'...")

        # Load analyzer module.
        analyzer_module = importlib.import_module(analyzer, "analyzers")

        # Extract analyzer attributes.
        analyzer_call = getattr(analyzer_module, analyzer_module.analyzer_call)
        output_format = "." + analyzer_module.analyzer_format
        parsed_data_path = config.parsed_data_path / case_id
        output_file = (parsed_data_path / analyzer).with_suffix(output_format)

        # Execute the analyzer.
        result = analyzer_call(parsed_data_path.as_posix(), output_file.as_posix())  # TODO: Make the input as pathlib.Path objects.

        if result != 0:
            logger.error("Execution failed, output not saved.")
            return result

        logger.info(f"Execution success, output saved in: {output_file.as_posix():s}")

        return result
