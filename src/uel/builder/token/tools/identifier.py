import sys
from string import ascii_letters
from unicodedata import lookup

__all__ = ["is_start", "is_identifier_center_char_or_end_char"]


def is_start(char: str) -> bool:
    if sys.version_info.major < 3:
        raise EnvironmentError(
            "Python 3's string is UTF-8,"
            "while Python 2's is not."
            "To ensure accuracy,"
            "Python 2 reports an error directly."
        )
    if char in ascii_letters:  # English
        return True
    elif '\u4e00' <= char <= '\u9fff':
        return True
    elif "_" == char:
        return True
    elif "$" == char:
        return True
    return False


def is_identifier_center_char_or_end_char(char: str) -> bool:
    return is_start(char) or char.isdigit()
