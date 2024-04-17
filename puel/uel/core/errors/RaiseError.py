from uel.core.errors.ThrowException import ThrowException
from uel.core.builder.Position import Position

class RaiseError:
    def __init__(self,et: type,em: str,pos: Position) -> None:
        ThrowException.throw(et(em,pos))
