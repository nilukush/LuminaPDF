import sys
from src.ui import cli, gui


def main():
    if len(sys.argv) > 1:
        cli.main()
    else:
        gui.main()


if __name__ == '__main__':
    main()
