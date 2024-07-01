from sys import argv

from uel.main import Main

__all__ = ["main"]


def main() -> None:
    Main().main(argv)
