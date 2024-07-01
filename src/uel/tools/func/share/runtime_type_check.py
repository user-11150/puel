from typing import Any

__all__ = ["runtime_type_check"]


def runtime_type_check(value: Any, *types: type) -> bool:
    return type(value) in types
