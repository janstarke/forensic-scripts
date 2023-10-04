import os
import argparse
import csv
import sys
import shutil
import coloredlogs, logging

__LOGGER__ = None


def logger():
    global __LOGGER__
    if not __LOGGER__:
        __LOGGER__ = logging.getLogger("windows-timeline")
        coloredlogs.install(level='INFO', logger=__LOGGER__)

    return __LOGGER__


def arguments():
    parser = argparse.ArgumentParser(
        prog="windows-timeline",
        description="create a timeline of a windows image, using dissect"
    )
    parser.add_argument('image_path')
    parser.add_argument('--overwrite', action='store_true', help='overwrite destination directory')
    parser.add_argument('--dialect',
                        choices=csv.list_dialects(),
                        default='unix',
                        help='select CSV dialect')
    args = parser.parse_args()

    return args