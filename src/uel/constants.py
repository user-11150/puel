from uel.builder.tokenize import Token

__all__ = ["Token", "File", "Color"]


class File:
    FILE_ENCODING = "UTF-8"


class Color:
    RED = "\033[31m"
    RESET = "\033[0m"
