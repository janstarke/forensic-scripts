import os
import shutil
import sys

from dissect.target import Target
from dissect.target.exceptions import UnsupportedPluginError

from utils import TxtFile, CsvFileFactory
from utils.cli import logger


class HostAnalyzer:
    def __init__(self, image_path: str, overwrite: bool = False):
        super(HostAnalyzer, self).__init__()
        self.__target = Target.open(image_path)
        self.__target.apply()
        self.__overwrite = overwrite
        self.__dst_dir = self.__create_destination_directory()

    def write_hostinfo(self):
        usernames = [f"{u.domain or u.hostname}\\{u.name}" for u in self.__target.users()]
        TxtFile(self.__dst_dir, "hostinfo") \
            .store(f"hostname     = {self.__target.hostname}{os.linesep}") \
            .store(f"domain       = {self.__target.domain}{os.linesep}") \
            .store(f"version      = {self.__target.version}{os.linesep}") \
            .store(f"install_date = {self.__target.install_date}{os.linesep}") \
            .store(f"language     = {self.__target.language}{os.linesep}") \
            .store(f"timezone     = {self.__target.timezone}{os.linesep}") \
            .store(f"ips          = {self.__target.ips}{os.linesep}") \
            .store(f"users        = {usernames}{os.linesep}")

    def invoke_plugin(self, plugin, csv_dialect: str):
        csv_factory = CsvFileFactory(self.__dst_dir, csv_dialect)
        try:
            plugin(self.__target).to_csv(csv_factory)
            logger().info(f"run of {plugin.__name__} was successful")
        except UnsupportedPluginError as e:
            logger().warning(f"{plugin.__name__}: {e.root_cause_str()}")

    def __create_destination_directory(self):
        logger().info(f"found image with hostname '{self.__target.hostname}'; creating target directory for it")
        dst = os.path.join(os.curdir, self.__target.hostname)
        if os.path.exists(dst):
            if self.__overwrite:
                logger().info(f"target directory '{dst}' exists already, deleting it")
                shutil.rmtree(dst)
            else:
                logger().error(f"target directory '{dst}' exists already, exiting")
                sys.exit(1)
        os.makedirs(dst)
        return dst
