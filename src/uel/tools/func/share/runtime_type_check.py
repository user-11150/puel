from typing import Any


def runtime_type_check(value: Any, *types: type) -> bool:
    return type(value) in types
