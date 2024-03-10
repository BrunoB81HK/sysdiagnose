# Analyzers

## Adding an analyzer

To add an analyzer, simply add a python file to this directory.

To be valid, the file must include the following attributes and functions:
* `analyzer_description: str`
* `analyzer_format: str`
* `main(parsed_data_path: pathlib.Path, filename: pathlib.Path) -> int`

The typical structure of the file should look a bit like this:

```python
import pathlib

# ----- definition for analyze command -----#
# -----          DO NOT DELETE         -----#

analyzer_description = "The description of the analyzer."
analyzer_format = "md"


def main(parsed_data_path: pathlib.Path, filename: pathlib.Path) -> int:
    ...

```
