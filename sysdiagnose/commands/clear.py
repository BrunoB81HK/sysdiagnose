import argparse


def add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "clear",
        help="Clear all the app cache.",
    )

    parser.add_argument(
        "-y",
        dest="auto_yes",
        action="store_true",
        help="automatically accept the prompt",
    )

    parser.set_defaults(func=main)

    return parser


def main(args: argparse.Namespace) -> int:
    if args.auto_yes:
        clear(True)

    valid_choice_map = {
        "yes": True,
        "ye": True,
        "y": True,
        "no": False,
        "n": False,
    }
    prompt = "This will erase all the app cache, including the extracted, parsed and analyzed data. Are you sure you want to proceed? [y/n]: "
    while (choice := input(prompt).lower()) not in valid_choice_map:
        print(f"'{choice:s}' is not a valid choice.")

    return clear(valid_choice_map[choice])


def clear(clear_app_cache: bool) -> int:
    # Import the related modules.
    import shutil

    from ..utils import logging
    from ..utils import paths

    # Get the logger.
    logger = logging.get_logger()

    if not clear_app_cache:
        logger.info("The clearing of the app cache was aborted.")
        return 0

    logger.info("Clearing the app cache...")

    paths.cases_file.write_text("cases: {}\n")
    paths.log_file.write_text("")

    shutil.rmtree(paths.data_path)
    shutil.rmtree(paths.parsed_data_path)

    logger.info("App cache cleared!")
    return 0
