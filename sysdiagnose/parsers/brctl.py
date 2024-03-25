"""
Script to parse the brctl-container-list.txt and brctl-dump.txt files
Author: Emilien Le Jamtel
"""

import pathlib
import re
import typing

from sysdiagnose.utils import version

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "Parsing brctl files"
parser_version = "1.0.0"
parser_input = "brctl"


def main(path: pathlib.Path, ios_version: version.Version = version.v13) -> None | dict:
    brctl_container_list_file = path / "brctl-container-list.txt"
    brctl_dump_file = path / "brctl-dump.txt"

    container_list_file_content = parse_list_file(brctl_container_list_file)
    dump_file_content = parse_dump_file(brctl_dump_file)

    return {**container_list_file_content, **dump_file_content}


def parse_list_file(container_list_file: pathlib.Path) -> dict[str, list[dict[str, str]]]:
    pattern = r"id:(?P<id>[^ ]*) localizedName:'(?P<localizedName>[^']*)' documents:'(?P<documents>[^']*)' \[(?P<privacy>[^:]*):(?P<status>[^\]]*)\] clients: (?P<clients>.*)"

    return {
        "containers": [
            {
                "id": match[0],
                "localizedName": match[1],
                "documents": match[2],
                match[3]: match[4],
                "clients": match[5],
            }
            for match in re.findall(pattern, container_list_file.read_text())
        ]
    }


def parse_dump_file(dump_file: pathlib.Path) -> dict[str, typing.Any]:
    # Parse the file.
    section = "header"
    dump = {section: ""}
    lines = dump_file.read_text().splitlines(True)

    for i, line in enumerate(lines):
        if line.strip() == "-----------------------------------------------------":
            section = lines[i - 1].strip()
            dump[section] = ""

        else:
            dump[section] += line

    # Retrieve some keys.
    boot_history_key = [key for key in dump.keys() if key.startswith("boot_history")][0]
    container_keys = [key for key, value in dump.items() if "+ app library:" in value]

    # Parsing different sections.
    # header
    header = parse_header(dump["header"])

    # boot_history
    boot_history = parse_boot_history(dump[boot_history_key])

    # server_state
    server_state = parse_server_state(dump["server_state"])

    # client_state
    client_state = parse_client_state(dump["client_state"])

    # system
    system = parse_system_scheduler(dump["system"])

    # scheduler
    scheduler = parse_system_scheduler(dump["scheduler"])

    # applibrary
    applibrary = parse_app_library(dump, container_keys)

    # server_items
    server_items = parse_server_items(dump, container_keys)

    # app library IDs by App ID
    app_library_id, app_ids = parse_apps_monitor(dump["apps monitor"])

    # Putting together all the parsed data.
    return {
        "header": header,
        "boot_history": boot_history,
        "server_state": server_state,
        "client_state": client_state,
        "system": system,
        "scheduler": scheduler,
        "applibrary": applibrary,
        "server_items": server_items,
        "app_library_id": app_library_id,
        "app_ids": app_ids,
    }


def parse_header(header: str) -> dict[str, str]:
    # Define a regular expression to match the key-value pairs.
    pattern = r"([\w ]+):\s+(.+)(?:\n|$)"

    # Find all the matches in the content.
    matches = re.findall(pattern, header)

    # Loop through the matches and add them to the output dictionary.
    output = dict()
    for key, value in matches:
        # If the value contains a comma, split it into a list.
        if "," in value:
            value = value.split(", ")

        # If the value contains brackets, remove them.
        if value.startswith("<") and value.endswith(">"):
            value = value[1:-1]

        # Add the key-value pair to the output dictionary.
        output[key.strip()] = value

    pattern = r"dump taken at (.*?) \[account=(\d+)\] \[inCarry=(\w+)\] \[home=(.+)\]"

    # Find the match in the content
    match = re.search(pattern, header)

    # Check if there is a match
    if match:
        # save the values
        output["timestamp"] = match.group(1)
        output["account"] = match.group(2)
        output["inCarry"] = match.group(3)
        output["home"] = match.group(4)

    # Return the dictionnary.
    return output


def parse_boot_history(boot_history: str) -> list[dict[str, str]]:
    # Define the regex pattern.
    pattern = r"\[(.+?)\] OS:(.+?) CloudDocs:(.+?) BirdSchema:(.+?) DBSchema:(.+) DeviceID:(.+)"

    # Loop through each line.
    result = list()
    for line in boot_history.splitlines():
        if match := re.search(pattern, line):
            result.append(
                {
                    "date": match.group(1),
                    "OS": match.group(2),
                    "CloudDocs": match.group(3),
                    "BirdSchema": match.group(4),
                    "DBSchema": match.group(5),
                    "DeviceID": match.group(6),
                }
            )
    # Return the result list.
    return result


def parse_server_state(server_state: str) -> dict[str, str | dict]:
    # Define the regex pattern.
    pattern = r"(last-sync|nextRank|minUsedTime):(.+?)(?=\s|$)"

    # Use re.findall to get all the matches as a list of tuples.
    matches = re.findall(pattern, server_state)

    # Loop through the matches
    output = dict()
    for field, value in matches:
        # Replace any dashes with underscores in the field name.
        field = field.replace("-", "_")

        # If the field is shared_db, create a nested dictionary for its value.
        if field == "shared_db":
            value = dict()

        # Add the field-value pair to the output dictionary.
        output[field] = value

    # Print the output dictionary
    return output


def parse_client_state(client_state: str) -> dict[str, int | float | str]:
    # Define the regex pattern.
    pattern = r"\s*(\w+)\s*=\s*(.*);"

    # Iterate over each line in the data.
    output = dict()
    for line in client_state.splitlines():
        # Use regular expressions to match key-value pairs.
        if match := re.match(pattern, line):
            key, value = match.groups()

            # Remove any quotes from the value.
            value = value.strip('"')

            # Try to convert the value to an integer or float.
            try:
                output[key] = int(value)
            except ValueError:
                try:
                    output[key] = float(value)
                except ValueError:
                    output[key] = value

    return output


def parse_system_scheduler(input: str) -> dict[str, str]:
    # Iterate over each line in the data.
    output = dict()
    for line in input.splitlines():
        # Removing ANSI escape codes.
        line = re.sub(r"\x1b\[[0-9;]*m", "", line).strip()

        if line.startswith("+"):
            key, value = line.split(":", 1)
            output[key.removeprefix("+ ")] = value.strip()

    return output


def parse_app_library(dump: dict[str, str], keys: list[str]) -> list[dict[str, str | list[str]]]:
    # Define the regex pattern.
    pattern = r"<(.*?)\[(\d+)\].*?ino:(\d+).*?apps:\{(.*?)\}.*?bundles:\{(.*?)\}"

    # Get all the app library lines.
    app_library_lines = [line for key in keys for line in dump[key].splitlines() if "+ app library" in line]

    # Iterate over each lines.
    return [
        {
            "library": match[0],
            "app_id": match[1],
            "ino": match[2],
            "apps": match[3].split("; "),
            "bundles": match[4].split(", "),
        }
        for line in app_library_lines
        if (match := re.search(pattern, line))
    ]


def parse_server_items(dump: dict[str, str], keys: list[str]) -> list[dict[str, str]]:
    # Define the regex pattern.
    pattern = r"-+([^\[]+)\[(\d+)\]-+"

    # Get all the app library lines.
    server_items_lines = [line for key in keys for line in dump[key].splitlines() if "----------------------" in line]

    # Iterate over each lines.
    return [
        {
            "library_name": match.group(1),
            "library_id": match.group(2),
        }
        for line in server_items_lines
        if (match := re.search(pattern, line))
    ]


def parse_apps_monitor(apps_monitor: str) -> dict[str, list[str]]:
    from sysdiagnose.utils import yaml

    # Convert the part string.
    def to_yaml_str(data: str) -> str:
        start = 0
        end = 0
        lines = [line.strip() for line in data.splitlines()]
        for i, line in enumerate(lines):
            if line.startswith("{"):
                start = i

            elif line.startswith("}"):
                end = i

        return "".join(
            [
                line.replace(";", ",")
                .replace("=", ":")
                .replace('"{(\\n', "[")
                .replace('\\n)}"', "]")
                .replace('\\"', '"')
                .replace("\\n", "")
                for line in lines[start : end + 1]
            ]
        )

    # Split the text into two parts.
    _, app_library_str, app_id_str = apps_monitor.split("=======================")

    app_library_str = to_yaml_str(app_library_str)
    app_id_str = to_yaml_str(app_id_str)

    return yaml.loads(app_library_str), yaml.loads(app_id_str)
