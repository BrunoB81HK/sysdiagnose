import argparse
import shutil

from . import config


logger = config.logger.getChild("clear")


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "clear",
        help="Clear all the app cache.",
    )
    parser.add_argument("-y", dest="auto_yes", action="store_true", help="automatically accept the prompt")
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    if not args.auto_yes:
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

        if not valid_choice_map[choice]:
            return 0

    config.cases_file.write_text("cases: {}\n")
    config.log_file.write_text("")
    shutil.rmtree(config.data_path)
    shutil.rmtree(config.parsed_data_path)

    return 0
