import os
import shutil
import sys

from dissect.target import Target
from dissect.target.exceptions import UnsupportedPluginError
from flow.record.adapter.csvfile import CsvfileWriter

from utils import TxtFile
from utils.cli import logger

class HostAnalyzer:
    def __init__(self, image_path: str, overwrite: bool = False):
        super(HostAnalyzer, self).__init__()
        self.__target = Target.open(image_path)
        self.__target.apply()
        self.__overwrite = overwrite
        self.__dst_dir = self.__create_destination_directory()
        self.__PLUGINS = [
            "amcache_install",
            "powershell_history",
            "prefetch",
            "runkeys",
            "usb",
            "userassist",
            "windowsuser"
        ]

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

    def invoke_plugins(self):
        for plugin in self.__PLUGINS:
            self.invoke_plugin(plugin)

    def invoke_plugin(self, plugin):
        try:
            records = getattr(self.__target, plugin)()
            self.write_csv(plugin, records)
            logger().info(f"run of {plugin} was successful")
        except UnsupportedPluginError as e:
            logger().warning(f"{plugin.__name__}: {e.root_cause_str()}")

    def write_csv(self, filename, records):
        if not filename.endswith(".csv"):
            filename += ".csv"

        writer = CsvfileWriter(os.path.join(self.__dst_dir, filename),
                               exclude=["hostname", "domain", "_generated", "_source", "_classification", "_version"])

        first_line = True
        for entry in records:

            # trick the writer into believing that the description has not changed
            if not first_line:
                writer.desc = entry._desc

            writer.write(entry)
            first_line = False

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
