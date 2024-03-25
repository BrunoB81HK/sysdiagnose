"""
Demo blank parser.
Author: david@autopsit.org
"""

import pathlib

from sysdiagnose.utils import version

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "Demo parser"
parser_version = "1.0.0"
parser_input = "demo_input_file"


def main(path: pathlib.Path, ios_version: version.Version = version.v13) -> None | dict:
    dict_object = dict()
    return dict_object
