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


def create_destination_directory(args, hostname: str):
    dst = os.path.join(os.curdir, hostname)
    if os.path.exists(dst):
        if args.overwrite:
            logger().info(f"target directory '{dst}' exists already, deleting it")
            shutil.rmtree(dst)
        else:
            logger().error(f"target directory '{dst}' exists already, exiting")
            sys.exit(1)
    os.makedirs(dst)
    return dst
