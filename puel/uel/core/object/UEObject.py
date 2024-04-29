from typing import Any, Tuple

class UEObject:
    def __repr__(self):
        return f"[<{self.__class__.__name__}> {repr(self.tp_str())[1:-1]}]"
    def tp_bytecode(self) -> Tuple[str, Any]:
        return "object", self

    def tp_str(self) -> Any:
        raise NotImplementedError
