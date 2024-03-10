# Parsers

## Adding an parser

To add an parser, simply add a python file to this directory.

To be valid, the file must include the following attributes and functions:
* `parser_description: str`
* `parser_input: str`
* `main(filepath: pathlib.Path) -> None | dict`

The typical structure of the file should look a bit like this:

```python
import pathlib

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "The description of the parser."
parser_input = "The case file dictionnary key containning all the paths of the files that needs to be parsed."


def main(filepath: pathlib.Path) -> None | dict:
    ...

```
