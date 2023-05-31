import sys
from datetime import datetime

import pypff
import argparse
import re
import codecs
import chardet
import coloredlogs
import logging


class Grepper:
    def __init__(self, pattern: re.Pattern, encoding: str):
        self.__pattern = pattern
        self.__encoding = encoding

    def grep_file(self, pff_file: pypff.file):
        pff_root_folder = pff_file.get_root_folder()
        self.__grep_item(pff_root_folder, "/")

    def __print_if_body_matches(self, parent_path: str, message: pypff.message, body: bytes):
        headers = message.get_transport_headers()
        if body:
            try:
                s = body.decode("UTF-8")
            except UnicodeDecodeError:
                try:
                    s = body.decode(self.__encoding)
                except UnicodeDecodeError:
                    encoding = chardet.detect(body)
                    logger.info("use encoding {encoding} with a confidence of {confidence}".format(**encoding))
                    try:
                        s = body.decode(encoding['encoding'])
                    except UnicodeDecodeError as e_chardet:
                        logger.warning("this did not work either. "
                                       "I'm falling back to {encoding} and will ignore errors".format(
                                        encoding=self.__encoding))
                        s = body.decode(self.__encoding, errors='ignore')
            if self.__pattern.search(s):
                print_match(parent_path, message, s)
                return True
            else:
                return False

    def __grep_item(self, item: pypff.item, parent_path: str):
        if isinstance(item, pypff.message):
            if self.__print_if_body_matches(parent_path, item, item.get_plain_text_body()):
                return
            if self.__print_if_body_matches(parent_path, item, item.get_rtf_body()):
                return
            try:
                if self.__print_if_body_matches(parent_path, item, item.get_html_body()):
                    return
            except:
                pass

        elif isinstance(item, pypff.folder):
            for si in item.sub_items:
                self.__grep_item(si, parent_path + "/" + item_name(item))


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="grep in .ost and .pst file timelines")

    parser.add_argument(
        'input',
        type=argparse.FileType('rb'),
        help="Input file")

    parser.add_argument(
        'pattern',
        type=str,
        help="pattern to search for")

    parser.add_argument("-i", "--ignore-case", help="do case insensitive pattern matching",
                        action="store_true", default=False)
    return parser


def item_name(item: pypff.item) -> any:
    if isinstance(item, pypff.folder):
        return item.get_name() or "id_{id:x}".format(id=item.get_identifier())
    else:
        return "id_{id:x}".format(id=item.get_identifier())


def print_match(parent_path: str, item: pypff.message, content: str):
    timestamp = item.get_client_submit_time() or item.get_creation_time()
    print("{timestamp}|{id:08x}|{path}|{subject}".format(
        timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        id=item.get_identifier(),
        path=parent_path,
        subject=item.get_subject()))


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
if __name__ == '__main__':
    args = create_parser().parse_args()
    __pff_file = pypff.file()
    __pff_file.open_file_object(args.input)

    # make sure that a codec with that name exists
    __codec_info = codecs.lookup(__pff_file.get_ascii_codepage().decode("ASCII"))
    if args.ignore_case:
        __pattern = re.compile(args.pattern, re.IGNORECASE)
    else:
        __pattern = re.compile(args.pattern)

    grepper = Grepper(__pattern, __codec_info.name)

    grepper.grep_file(__pff_file)
    __pff_file.close()
