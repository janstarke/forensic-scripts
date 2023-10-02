from abc import ABCMeta, abstractmethod
import csv


class ExportableItem(object):
    def __init__(self,
                 attributes: list,
                 timestamp: str):
        if timestamp not in attributes:
            raise SyntaxError(f"cannot sort by {timestamp}, because it is not an attribute")
        self.__timestamp = timestamp
        self.__attributes = attributes

    def __call__(self, cls):
        cls.timestamp_attribute = staticmethod(lambda: self.__timestamp)
        cls.attributes = staticmethod(lambda: self.__attributes)
        return cls


class AbstractExportableItem(object, metaclass=ABCMeta):
    def __init__(self, entries: list):
        self.__entries = entries

    def timestamp_attribute(self) -> str:
        pass

    def attributes(self) -> list:
        pass

    def to_csv(self, dst_file):
        self.__entries.sort(key=lambda e: e.__getattribute__(self.timestamp_attribute()))
        writer = csv.DictWriter(dst_file, fieldnames=self.attributes())

        for entry in self.__entries:
            writer.writerow(
                {k: v for (k, v) in map(lambda a: (a, entry.__getattribute__(a)), self.attributes())}
            )
