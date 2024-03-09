# Commands

## Adding a command

To add a command, simply add a python file to this directory.

To be valid, the file must include the following functions:
* `add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser`
* `main(args: argparse.Namespace) -> int`

The typical structure of the file should look a bit like this:

```python
import argparse

def add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        "<command name>",
        help="<command description>",
    )

    # Add the parser's arguments.
    parser.add_argument(
        ...
    )

    # Set the the function that is executed by the command.
    # This function should take the parsed arguments and return the command execution result code.
    parser.set_defaults(func=main)


def main(args: argparse.Namespace) -> int:
    ...

```
