import os

from utils import CsvFile


class CsvFileFactory:
    def __init__(self, basedir: str, dialect: str):
        self.__basedir = basedir
        self.__dialect = dialect

    def open_csv_file(self, basename: str, fields: list):
        if not basename.endswith(".csv"):
            basename += ".csv"
        return CsvFile(os.path.join(self.__basedir, basename), self.__dialect, fields)
