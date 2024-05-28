from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.object.UEBooleanObject import UEBooleanObject
from uel.core.object.UEObject import UEObject
from uel.tools.func.share.runtime_type_check import runtime_type_check


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

    def tp_equal(self, other):
        if (runtime_type_check(other, UEStringObject) and
                other.val == self.val):
            return UEBooleanObject(True)
        return UEBooleanObject(False)
