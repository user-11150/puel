from typing import Any

class UEObject:
    def tp_bytecode(self) -> Any:
        raise NotImplementedError

    def tp_str(self) -> Any:
        raise NotImplementedError
