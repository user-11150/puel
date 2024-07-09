from uel.builder.position import Position
from uel.errors.uelexception import UELException
import linecache
from uel.colors import RED, RESET

import wcwidth

__all__ = ["UELBuildtimeException"]


def hint(line, col, offset):
    hinted = " " * offset

    for char in line[0:col]:
        width = wcwidth.wcwidth(char)
        if width < 0:
            width = 0
        elif width == 0:
            width = 1
        hinted += " " * width
    hinted += "^"

    if not line:
        return "\n"

    return "\n" + (" " * offset) + line + hinted + "\n"


class UELBuildtimeException(UELException):
    def __init__(self, error_message: str, pos: Position):
        super().__init__(error_message)
        self.line = pos.ln
        self.file = pos.fn
        self.column = pos.col

    def __str__(self) -> str:
        oes: str = super().__str__()
        line = linecache.getline(self.file, self.line)
        pos_string = f"File {repr(self.file)}, line {self.line},\n"
        return f"""\
{pos_string}{hint(line, self.column, 2)}{oes}"""
