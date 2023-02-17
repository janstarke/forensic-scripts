import argparse
import os
import pylnk
from io import FileIO


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="create bodyfile from lnk files")

    parser.add_argument(
        'input',
        nargs='+',
        type=argparse.FileType('rb'),
        help="Input file")

    return parser


class BodyfileLine:
    def __init__(self, file: FileIO):
        __lnkfile = pylnk.open_file_object(file)
        self.__lnkname = os.path.basename(file.name)
        self.__local_path = __lnkfile.local_path or __lnkfile.network_path or __lnkfile.relative_path
        self.__access_time = __lnkfile.file_access_time
        self.__creation_time = __lnkfile.file_creation_time
        self.__modification_time = __lnkfile.file_modification_time
        self.__identifier = __lnkfile.birth_droid_file_identifier
        self.__size = __lnkfile.file_size

        lid = __lnkfile.link_target_identifier_data
        pass

    def __str__(self):
        bf3format = "0|{name} (referred to by {lnkname})|{inode}|{mode}|0|0|{size}|{atime}|{mtime}|-1|{crtime}"
        return bf3format.format(
            name=self.__local_path,
            lnkname=self.__lnkname,
            inode=self.__identifier,
            mode="r/rrwxrwxrwx",
            size=self.__size,
            atime=int(self.__access_time.timestamp()),
            mtime=int(self.__modification_time.timestamp()),
            crtime=int(self.__creation_time.timestamp())
        )


if __name__ == '__main__':
    args = create_parser().parse_args()
    for f in args.input:
        print(str(BodyfileLine(f)))
