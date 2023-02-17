import sys
from datetime import datetime

import pypff
import argparse
from striprtf.striprtf import rtf_to_text


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="display mails from .ost or .pst files")

    parser.add_argument(
        'input',
        type=argparse.FileType('rb'),
        help="Input file")

    parser.add_argument(
        'mail_id',
        type=str,
        help="mail id (hexadecimal number")

    parser.add_argument("-H", "--html", help="display the html body, if it exists. "
                                             "This is the default if nothing else was specified",
                        action="store_true", default=False)
    parser.add_argument("-T", "--text", help="display the raw txt body, if it exists, "
                                            "or try to extract from RTF if possible",
                        action="store_true", default=False)
    parser.add_argument("-R", "--rtf", help="display the rtf body, if it exists",
                        action="store_true", default=False)
    parser.add_argument("--headers", help="display mail headers",
                        action="store_true", default=False)
    return parser


def find_id(folder: pypff.folder, mail_id: int) -> pypff.message:
    for item in folder.sub_items:
        if isinstance(item, pypff.message):
            if item.get_identifier() == mail_id:
                return item
        elif isinstance(item, pypff.folder):
            result = find_id(item, mail_id)
            if result:
                return result


def find_id_in_file(file: pypff.file, mail_id: int) -> pypff.message:
    return find_id(file.get_root_folder(), mail_id)

def nl():
    sys.stdout.buffer.flush()
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == '__main__':
    args = create_parser().parse_args()
    __pff_file = pypff.file()
    __pff_file.open_file_object(args.input)

    __id = int(args.mail_id, 16)
    message = find_id_in_file(__pff_file, __id)

    if not (args.headers and args.html and args.txt and args.rtf):
        args.html = True

    if message:
        if args.headers:
            sys.stdout.write(message.get_transport_headers())
            nl()

        if args.text:
            if message.get_plain_text_body():
                sys.stdout.buffer.write(message.get_plain_text_body())
                nl()
            elif message.get_rtf_body():
                sys.stdout.buffer.write(rtf_to_text(message.get_rtf_body(), "cp1252", errors='surrogate'))
                nl()

        if args.rtf:
            if message.get_rtf_body():
                sys.stdout.buffer.write(message.get_rtf_body())
                nl()

        if args.html:
            if message.get_html_body():
                sys.stdout.buffer.write(message.get_html_body())
                nl()
    else:
        sys.stderr.write("message not found\n")

    __pff_file.close()
