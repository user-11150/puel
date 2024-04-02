"""
让一个函数只执行一次
"""

from ctypes import pointer
from ctypes import c_ulong

from typing import Any

def single_call(fn: Any) -> Any:
    run_count: Any = pointer(c_ulong(0))
    
    def inner(*args: Any, **kwargs: Any) -> Any:
        if 1 <= run_count.contents.value:
            raise RuntimeError("This function is called at most once.")
        result: Any = fn(*args, **kwargs)
        run_count.contents.value += 1
        return result
    return inner

