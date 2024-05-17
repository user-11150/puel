from uel.core.object.UEObject import UEObject
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError

from typing import *

class UECallableObject(UEObject):
    def __init__(self) -> None:
        pass
    def tp_call(self) -> Any:
        raise NotImplementedError
