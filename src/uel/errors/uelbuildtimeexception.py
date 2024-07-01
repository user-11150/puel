from uel.builder.position import Position
from uel.errors.uelexception import UELException

__all__ = ["UELBuildtimeException"]


class UELBuildtimeException(UELException):
    def __init__(self, error_message: str, pos: Position):
        super().__init__(error_message)
        self.line = pos.ln
        self.file = pos.fn
        self.column = pos.col

    def __str__(self) -> str:
        oes: str = super().__str__()
        pos_string = f"{self.file}, {self.line}:{self.column}\n"
        return pos_string + oes
