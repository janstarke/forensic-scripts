import utils
from utils import HostAnalyzer


def main():
    args = utils.cli.arguments()

    analyzer = HostAnalyzer(args.image_path, overwrite=args.overwrite)
    analyzer.write_hostinfo()
    analyzer.invoke_plugins()


if __name__ == '__main__':
    main()
