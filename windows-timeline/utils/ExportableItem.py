from abc import ABCMeta
from typing import Optional

from utils import CsvFileFactory


class ExportableItem(object):
    def __init__(self,
                 filename: str,
                 attributes: list,
                 timestamp: Optional[str]):
        if timestamp and timestamp not in attributes:
            raise SyntaxError(f"cannot sort by {timestamp}, because it is not an attribute")
        self.__filename = filename
        self.__timestamp = timestamp
        self.__attributes = attributes

    def __call__(self, cls):
        cls.timestamp_attribute = staticmethod(lambda: self.__timestamp)
        cls.attributes = staticmethod(lambda: self.__attributes)
        cls.filename = staticmethod(lambda: self.__filename)
        return cls


class AbstractExportableItem(object, metaclass=ABCMeta):
    def __init__(self, entries: list):
        self.__entries = entries

    def timestamp_attribute(self) -> str:
        pass

    def attributes(self) -> list:
        pass

    def filename(self) -> list:
        pass

    def to_csv(self, factory: CsvFileFactory):
        if self.timestamp_attribute():
            self.__entries.sort(key=lambda e: e.__getattribute__(self.timestamp_attribute()))

        csv_file = factory.open_csv_file(self.filename(), self.attributes())

        for entry in self.__entries:
            csv_file.writerow(entry)
