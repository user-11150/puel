import sys
from typing import *

from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.errors.raiseerror import RaiseError

__all__ = ["throw"]


@overload
def throw(e: UELRuntimeError) -> None:
    ...


@overload
def throw(e: type[UELRuntimeError], string: str) -> None:
    ...


def throw(e: Any, string: Any = None):
    if type(e) is type:
        obj = e(string)

    RaiseError(obj.__class__, obj.error_message)
