"""
Script to print from Accessibility TCC logs
Author: david@autopsit.org
"""

import pathlib

from sysdiagnose.utils import version

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "Parsing Accessibility TCC logs"
parser_version = "1.0.0"
parser_input = "Accessibility-TCC"


def main(path: pathlib.Path, ios_version: version.Version = version.v13) -> None | dict:
    from sysdiagnose.utils import sqlite

    return sqlite.load_db(path)
