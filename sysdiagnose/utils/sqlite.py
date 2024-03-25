"""
Module with functions to handle sqlite databases.
"""

import pathlib
import sqlite3


def __validate_value(value: object) -> str | int | float | bool:
    if not isinstance(value, (str, int, float, bool)):
        value = str(value)
    return value


def load_db(filepath: pathlib.Path) -> None | dict:
    try:
        with sqlite3.connect(filepath) as database_con:
            cursor = database_con.cursor()

            cursor.execute("select name from sqlite_master where type = 'table'")
            tables = [table[0] for table in cursor.fetchall()]

            data = dict()
            for table in tables:
                cursor.execute(f"SELECT * FROM '{table:s}'")
                column_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                data[table] = [
                    {element_name: __validate_value(element) for element_name, element in zip(column_names, row)} for row in rows
                ]

        return data

    except Exception as e:
        from sysdiagnose.utils import logging

        logger = logging.get_logger()
        logger.error(f"Could not parse {filepath.as_posix():s}. Reason: {str(e)}")

    return None
