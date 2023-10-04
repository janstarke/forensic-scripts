import csv
import os


class TxtFile:
    def __init__(self, basedir: str, basename: str):
        if not basename.endswith(".txt"):
            basename += ".txt"

        self.__dstfile = os.path.join(basedir, basename)

        # truncate the file
        self.__file = open(self.__dstfile, "w")

    def store(self, data):
        if isinstance(data, str):
            self.__file.write(data)
        elif isinstance(data, list):
            self.__file.writelines(data)
        else:
            writer = csv.writer(self.__file)
            for item in data:
                writer.writerow([item.path])
        return self
