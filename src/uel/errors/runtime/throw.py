import sys
from typing import *

from uel.errors.runtime.uelruntimeerror import UELRuntimeError

__all__ = ["throw"]


@overload
def throw(e: UELRuntimeError) -> None:
    ...


@overload
def throw(e: type[UELRuntimeError], string: str) -> None:
    ...


def throw(e: Any, string: Any = None):
    if type(e) is type:
        e = e(string)
    sys.stderr.write(str(e))
    raise SystemExit
