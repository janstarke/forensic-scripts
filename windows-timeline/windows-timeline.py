import argparse
import csv
import sys

import coloredlogs
import logging
import os
import shutil
from dissect.target import Target, container, volume

from tlnobjects import UserAssist

def arguments():
    parser = argparse.ArgumentParser(
        prog="windows-timeline",
        description="create a timeline of a windows image, using dissect"
    )
    parser.add_argument('image_path')
    parser.add_argument('--overwrite', action='store_true', help='overwrite destination directory')
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


def store_users(users, dst_file):
    with open(dst_file, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['name', 'sid', 'home', 'domain', 'hostname'])

        writer.writeheader()
        for user in users:
            writer.writerow({
                'name': user.name,
                'sid': user.sid,
                'home': user.home,
                'domain': user.domain,
                'hostname': user.hostname
            })


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

    store(t.version, os.path.join(dstdir, "version.txt"))
    store(t.ips, os.path.join(dstdir, "ips.txt"))
    store_users(t.users(), os.path.join(dstdir, "users.csv"))
    ua = UserAssist(t)
    ua.to_csv(open(os.path.join(dstdir, "userassist.csv"), "w"))