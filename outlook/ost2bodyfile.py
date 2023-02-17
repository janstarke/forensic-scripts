import sys
from datetime import datetime

import pypff
import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="create .ost and .pst file timelines")

    parser.add_argument(
        'input',
        type=argparse.FileType('rb'),
        help="Input file")

    return parser


def message_size(message: pypff.message) -> int:
    size = 0

    size += len(message.get_plain_text_body() or "")
    size += len(message.get_rtf_body() or "")
    size += len(message.get_html_body() or "")

    for a in message.attachments:
        size += a.get_size()
    return size


def item_name(item: pypff.item) -> any:
    if isinstance(item, pypff.folder):
        return item.get_name() or "id_{id:x}".format(id=item.get_identifier())
    else:
        return "id_{id:x}".format(id=item.get_identifier())


class Bodyfile3Line:

    def __init__(self, item: pypff.item, parent_path: str):
        if isinstance(item, pypff.message):
            self.__crtime = int(item.get_creation_time().timestamp())
            self.__atime = int((item.get_delivery_time() or datetime.fromtimestamp(-1)).timestamp())
            self.__mtime = int((item.get_modification_time() or datetime.fromtimestamp(-1)).timestamp())
            self.__subject = "{id}: {subject}".format(
                id=parent_path + "/" + item_name(item),
                subject=item.get_subject())
            self.__mode = "r/rwxrwxrwx"
            self.__identifier = str(item.get_identifier())
            self.__size = message_size(item)
            self.__ignore = False
        elif isinstance(item, pypff.folder):
            self.__crtime = -1
            self.__atime = -1
            self.__mtime = -1
            self.__mode = "d/drwxrwxrwx"
            self.__subject = "{name}".format(name=item.get_name())
            self.__identifier = str(item.get_identifier())
            self.__size = 0
            self.__ignore = False
        else:
            self.__subject = "IGNORE THIS"
            self.__identifier = "IGNORE THIS"
            self.__mode = "IGNORE THIS"
            self.__size = "IGNORE THIS"
            self.__atime = "IGNORE THIS"
            self.__mtime = "IGNORE THIS"
            self.__crtime = "IGNORE THIS"
            #sys.stderr.write("no support for type: {typename}\n".format(typename=type(item).__name__))
            self.__ignore = True

    def ignore(self):
        self.__ignore

    def __str__(self):
        assert (not self.ignore())
        bf3format = "0|{name}|{inode}|{mode}|0|0|{size}|{atime}|{mtime}|-1|{crtime}"
        return bf3format.format(
            name=self.__subject,
            inode=self.__identifier,
            mode=self.__mode,
            size=self.__size,
            atime=self.__atime,
            mtime=self.__mtime,
            crtime=self.__crtime
        )


def print_item_timeline(item: pypff.item, parent_path: str):
    line = Bodyfile3Line(item, parent_path)
    if not line.ignore():
        print(line)

    my_name = item_name(item)
    x = item.sub_items
    for si in item.sub_items:
        print_item_timeline(si, parent_path + "/" + my_name)


def print_timeline(pff_file):
    pff_root_folder = pff_file.get_root_folder()
    print_item_timeline(pff_root_folder, "/")


if __name__ == '__main__':
    args = create_parser().parse_args()
    __pff_file = pypff.file()
    __pff_file.open_file_object(args.input)
    print_timeline(__pff_file)
    __pff_file.close()


