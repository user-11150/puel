from typing import Any, Tuple, TypeVar

T = TypeVar("T")


class UEObject:

    def __repr__(self):
        return self.tp_str()

    def tp_bytecode(self) -> Tuple[str, Any]:
        return "object", self

    def tp_str(self) -> Any:
        return_string = hex(id(self))
        return f"<{self.__class__.__name__} {return_string}>"

    def tp(self, typ: type[T]) -> T:
        return self  # type: ignore
