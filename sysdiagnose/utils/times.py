"""
Module with functions to handle different types of times.
"""

import datetime


def macepoch2time(macepoch: float) -> datetime.datetime:
    """
    Convert install_date from Cocoa EPOCH to UTC.
    Difference between COCOA and UNIX epoch is 978307200 seconds.
    """
    unix_epoch = macepoch + 978307200
    utc_time = datetime.datetime.utcfromtimestamp(unix_epoch)
    return utc_time
