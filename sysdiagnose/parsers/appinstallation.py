"""
Script to print connection info from logs/appinstallation/AppUpdates.sqlite.db (iOS12)
New version of iOS store data into logs/appinstallation/appstored.sqlitedb
Author: david@autopsit.org

PID: Encoded in Little Endian?
TODO: Add support of iOS13...
"""

import pathlib

from sysdiagnose.utils import version

# ----- definition for parse command -----#
# -----         DO NOT DELETE        -----#

parser_description = "Parsing app installation logs"
parser_version = "2.0.0"
parser_input = "appinstallation"


def main(path: pathlib.Path, ios_version: version.Version = version.v13) -> None | dict:
    if ios_version.major >= 13:
        # Parse the file.
        from sysdiagnose.utils import sqlite

        return sqlite.load_db(path)

    else:
        # Print the file's content.
        # FIXME: Doesn't parse, only print.
        import sqlite3

        from sysdiagnose.utils import logging
        from sysdiagnose.utils import times

        logger = logging.get_logger()
        logger.warning(f"iOS {ios_version:d} and under is not supported, printing instead.")

        try:
            appinstalldb = sqlite3.connect(path)
            cursor = appinstalldb.cursor()
            for row in cursor.execute("SELECT pid, bundle_id, install_date FROM app_updates"):
                pid, bundle_id, install_date = row
                utc_time = times.macepoch2time(install_date)

                # Print the result.
                # TODO: Upgrade the print if not handled.
                print(f"{pid}, {bundle_id}, {utc_time}")

        except Exception as e:
            logger.error(f"Could not parse {path.as_posix():s}. Reason: {str(e)}")
