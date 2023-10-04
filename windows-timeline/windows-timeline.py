import inspect

import coloredlogs
import logging
import os
from dissect.target import Target
from dissect.target.exceptions import UnsupportedPluginError

import tlnobjects
import utils
from utils import CsvFileFactory, TxtFile


def main():
    args = utils.cli.arguments()

    t = Target.open(args.image_path)
    t.apply()

    utils.cli.logger().info("found image with hostname '{hostname}'; creating target directory for it".format(hostname=t.hostname))
    dstdir = utils.cli.create_destination_directory(args, t.hostname)

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
            utils.cli.logger().warning(f"{obj.__name__}: {e.root_cause_str()}")


if __name__ == '__main__':
    main()
