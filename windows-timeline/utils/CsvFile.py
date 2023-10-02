import csv


class CsvFile:
    def __init__(self, filename: str, fields: list):
        self.__fields = fields
        self.__writer = csv.DictWriter(open(filename, "w"), fieldnames=fields)

    def writerow(self, record):
        self.__writer.writerow(
            {k: v for (k, v) in map(lambda a: (a, record.__getattribute__(a)), self.__fields)}
        )