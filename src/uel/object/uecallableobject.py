from typing import *

from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.object.ueobject import UEObject
from uel.tools.func.share.runtime_type_check import runtime_type_check


class UECallableObject(UEObject):
    def __init__(self) -> None:
        pass

    def tp_call(self, *args, **kwargs) -> Any:
        raise NotImplementedError
