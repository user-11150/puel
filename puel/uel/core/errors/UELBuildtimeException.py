from uel.core.errors.UELException import UELException
from uel.core.builder.Position import Position

class UELBuildtimeException(UELException):
    def __init__(self,error_message: str,pos: Position):
        super().__init__(error_message)
        self.line = pos.ln
        self.file = pos.fn
    def __str__(self) -> str:
        oes: str = super().__str__()
        pos_string = f"{self.file}:{self.line}\n"
        return pos_string + oes
