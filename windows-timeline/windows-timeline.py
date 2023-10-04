import inspect

import tlnobjects
import utils
from utils import HostAnalyzer


def main():
    args = utils.cli.arguments()

    analyzer = HostAnalyzer(args.image_path, overwrite=args.overwrite)
    analyzer.write_hostinfo()

    for _, plugin in inspect.getmembers(tlnobjects, inspect.isclass):
        analyzer.invoke_plugin(plugin, csv_dialect=args.dialect)


if __name__ == '__main__':
    main()
