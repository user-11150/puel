from typing import Any, Tuple, TypeVar

T = TypeVar("T")


class UEObject:

    _create: Any

    def __new__(cls, *args) -> "UEObject":
        obj = object.__new__(cls)
        obj._create = args
        return obj

    def __reduce__(self) -> Tuple[type, Tuple[Any, ...]]:
        return self.__class__, self._create

    def __repr__(self):
        return self.tp_str()

    def tp_bytecode(self) -> Tuple[str, Any]:
        return "object", self

    def tp_str(self) -> Any:
        return_string = hex(id(self))
        classname = self.__class__.__name__[2:-6]
        return f"[{classname.lower()} {classname.title()}]"

    def tp(self, typ: type[T]) -> T:
        return self  # type: ignore
