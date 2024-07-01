"""
让一个函数只执行一次
"""

from ctypes import c_ulong, pointer
from typing import *

T = ParamSpec("T")
R = TypeVar("R")

__all__ = ["single_call"]


def single_call(fn: Callable[T, R]) -> Callable[T, R]:
    run_count: Any = pointer(c_ulong(0))

    def inner(*args: Any, **kwargs: Any) -> Any:
        if 1 <= run_count.contents.value:
            raise RuntimeError("This function is called at most once.")
        result: Any = fn(*args, **kwargs)
        run_count.contents.value += 1
        return result

    return inner
