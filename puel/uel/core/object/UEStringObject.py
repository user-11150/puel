from uel.core.object.UEObject import UEObject
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError

class UEStringObject(UEObject):
    def tp_str(self):
        return self.val
    def tp_add(self, other):
        if runtime_type_check(other, UEStringObject) \
             or runtime_type_check(other, str):
            if runtime_type_check(other, UEStringObject):
                return UEStringObject(self.val + other.val)
            else:
                return UEStringObject(self.val + other)
        else:
            throw(UELRuntimeError("Type Error: Cannot add"))
    def __init__(self, string):
        self.val = string
