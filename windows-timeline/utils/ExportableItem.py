import os
from abc import ABCMeta

from dissect.target import Target
from flow.record.adapter.csvfile import CsvfileWriter


class ExportableItem(object):
    def __init__(self,
                 filename: str,
                 datasource: str,
                 attributes: list[str]):
        self.__filename = filename
        self.__attributes = attributes
        self.__datasource = datasource

    def __call__(self, cls):
        cls.attributes = staticmethod(lambda: self.__attributes)
        cls.filename = staticmethod(lambda: self.__filename)
        cls.datasource = staticmethod(lambda: self.__datasource)
        return cls


class AbstractExportableItem(object, metaclass=ABCMeta):
    def __init__(self, target: Target):
        self.__entries = [e for e in getattr(target, self.datasource())()]

    def timestamp_attribute(self) -> str:
        pass

    def attributes(self) -> list:
        pass

    def filename(self) -> list:
        pass

    def to_csv(self, basedir: str):

        filename = self.filename()
        if not filename.endswith(".csv"):
            filename += ".csv"

        writer = CsvfileWriter(os.path.join(basedir, filename),
                               exclude=["hostname", "domain", "_generated", "_source", "_classification", "_version"])

        first_line = True
        for entry in self.__entries:

            # trick the writer into believing that the description has not changed
            if not first_line:
                writer.desc = entry._desc

            writer.write(entry)
            first_line = False
