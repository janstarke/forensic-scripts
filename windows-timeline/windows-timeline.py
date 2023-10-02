import argparse
import csv
import sys

import coloredlogs
import logging
import os
import shutil
from dissect.target import Target

from tlnobjects import *
from utils import CsvFileFactory


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


def store(data, dst_file):
    with open(dst_file, "w") as f:
        if isinstance(data, str):
            f.write(data)
        elif isinstance(data, list):
            f.writelines(data)
        else:
            writer = csv.writer(f)
            for item in data:
                writer.writerow([item.path])


if __name__ == '__main__':
    logger = logging.getLogger("windows-timeline")
    coloredlogs.install(level='INFO')

    args = arguments()

    t = Target.open(args.image_path)
    t.apply()

    logger.info("found image with hostname '{hostname}'; creating target directory for it".format(hostname=t.hostname))
    dstdir = os.path.join(os.curdir, t.hostname)
    if os.path.exists(dstdir):
        if args.overwrite:
            logger.warning("target directory '{dstdir}' exists already, deleting it".format(dstdir=dstdir))
            shutil.rmtree(dstdir)
        else:
            logger.error("target directory '{dstdir}' exists already, exiting".format(dstdir=dstdir))
            sys.exit(1)
    os.makedirs(dstdir)

    factory = CsvFileFactory(dstdir, args.dialect)

    store(t.version, os.path.join(dstdir, "version.txt"))
    store(t.ips, os.path.join(dstdir, "ips.txt"))

    UserAssist(t).to_csv(factory)
    WindowsUser(t).to_csv(factory)
