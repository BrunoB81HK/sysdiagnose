import pathlib

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "Parsing Accessibility TCC logs."
parser_input = "Accessibility-TCC"


def main(filepath: pathlib.Path) -> None | dict:
    from sysdiagnose.utils import sqlite

    return sqlite.sqlite2dict(filepath)
