from uel.core.builder.Position import Position
from uel.core.errors.ThrowException import ThrowException


class RaiseError:

    def __init__(self, et: type, em: str, pos: Position) -> None:
        ThrowException.throw(et(em, pos))
