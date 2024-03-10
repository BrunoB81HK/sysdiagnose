import importlib
import pathlib
import types

__all__ = (
    "get_all_analyzers",
    "get_all_cases",
    "get_all_parsers",
    "all_analyzers",
    "all_cases",
    "all_parsers",
)


def __validate_module(module: types.ModuleType, module_type: str) -> bool:
    module_attr_mapping = {
        "analyzers": [
            "analyzer_description",
            "analyzer_format",
        ],
        "parsers": [
            "parser_description",
            "parser_input",
        ],
    }

    is_valid = True

    for attr in module_attr_mapping.get(module_type, []):
        is_valid &= hasattr(module, attr)

    return is_valid


def get_all_analyzers() -> dict[str]:
    analyzers_root = pathlib.Path(__file__).parent.parent / "analyzers"

    analyzers = dict()
    for analyzer_file in analyzers_root.glob("[!_]*.py"):
        module = importlib.import_module(f"sysdiagnose.analyzers.{analyzer_file.stem:s}")

        if __validate_module(module, "analyzers"):
            analyzers[analyzer_file.stem] = {
                "description": module.analyzer_description,
            }

    return analyzers


def get_all_cases() -> dict[str]:
    from . import paths
    from . import yaml

    return yaml.load(paths.cases_file)["cases"]


def get_all_parsers() -> dict[str]:
    parsers_root = pathlib.Path(__file__).parent.parent / "parsers"

    parsers = dict()
    for parser_file in parsers_root.glob("[!_]*.py"):
        module = importlib.import_module(f"sysdiagnose.parsers.{parser_file.stem:s}")

        if __validate_module(module, "parsers"):
            parsers[parser_file.stem] = {
                "description": module.parser_description,
                "input": module.parser_input,
            }

    return parsers


all_analyzers = get_all_analyzers().keys()
all_cases = get_all_cases().keys()
all_parsers = get_all_parsers().keys()
