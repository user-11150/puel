from uel.builder.position import Position
from uel.errors.throwexception import ThrowException

__all__ = ["RaiseError"]


class RaiseError:
    def __init__(self, et: type, em: str, pos: Position = None) -> None:
        if pos is not None:
            ThrowException.throw(et(em, pos))
        else:

            ThrowException.throw(et(em))
