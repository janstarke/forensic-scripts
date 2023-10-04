import argparse
import csv
import inspect
import sys

import coloredlogs
import logging
import os
import shutil
from dissect.target import Target
from dissect.target.exceptions import UnsupportedPluginError

import tlnobjects
from tlnobjects import *
from utils import CsvFileFactory, TxtFile


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


def create_destination_directory(hostname: str):
    dst = os.path.join(os.curdir, hostname)
    if os.path.exists(dst):
        if args.overwrite:
            logger.info(f"target directory '{dst}' exists already, deleting it")
            shutil.rmtree(dst)
        else:
            logger.error(f"target directory '{dst}' exists already, exiting")
            sys.exit(1)
    os.makedirs(dst)
    return dst


if __name__ == '__main__':
    logger = logging.getLogger("windows-timeline")
    coloredlogs.install(level='INFO')

    args = arguments()

    t = Target.open(args.image_path)
    t.apply()

    logger.info("found image with hostname '{hostname}'; creating target directory for it".format(hostname=t.hostname))
    dstdir = create_destination_directory(t.hostname)

    factory = CsvFileFactory(dstdir, args.dialect)

    usernames = [f"{u.domain or u.hostname}\\{u.name}" for u in t.users()]
    TxtFile(dstdir, "hostinfo") \
        .store(f"hostname     = {t.hostname}{os.linesep}") \
        .store(f"domain       = {t.domain}{os.linesep}") \
        .store(f"version      = {t.version}{os.linesep}") \
        .store(f"install_date = {t.install_date}{os.linesep}") \
        .store(f"language     = {t.language}{os.linesep}") \
        .store(f"timezone     = {t.timezone}{os.linesep}") \
        .store(f"ips          = {t.ips}{os.linesep}") \
        .store(f"users        = {usernames}{os.linesep}")

    for _, obj in inspect.getmembers(tlnobjects, inspect.isclass):
        try:
            obj(t).to_csv(factory)
        except UnsupportedPluginError as e:
            logger.warning(f"{obj.__name__}: {e.root_cause_str()}")
