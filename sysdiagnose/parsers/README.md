# Parsers

## Adding an parser

To add an parser, simply add a python file to this directory.

To be valid, the file must include the following attributes and functions:
* `parser_description: str`
* `parser_version: str`
* `parser_input: str`
* `main(path: pathlib.Path) -> None | dict`

The typical structure of the file should look a bit like this:

```python
import pathlib

from sysdiagnose.utils import version

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "The description of the parser."
parser_version = "1.0.0"
parser_input = "The case file dictionnary key containing all the paths of the files that needs to be parsed."


def main(path: pathlib.Path, ios_version: version.Version = version.Version(13, 0, 0)) -> None | dict:
    ...

```
