from typing import Any


def runtime_type_check(value: Any, type_: type) -> bool:
    return type(value) is type_
