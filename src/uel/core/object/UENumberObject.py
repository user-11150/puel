import typing as t

from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.core.object.UEBooleanObject import UEBooleanObject
from uel.core.object.UEObject import UEObject

class UENumberObject(UEObject):

    def tp_str(self):
        return str(self.val)

    def tp_add(self, other):
        return UENumberObject(
            self.val
         + (other.val
              if isinstance(other, UENumberObject)
              else other)
        )
    def tp_minus(self, other):
        return UENumberObject(
            self.val
         - (other.val
              if isinstance(other, UENumberObject)
              else other)
        )
    def tp_mult(self, other):
        return UENumberObject(
            self.val
         * (other.val
              if isinstance(other, UENumberObject)
              else other)
        )
    def tp_div(self, other):
        return UENumberObject(
            self.val
         / (other.val
              if isinstance(other, UENumberObject)
              else other)
        )
    
    def tp_equal(self, other):
        if not runtime_type_check(other, type(self)):
            return UEBooleanObject(False)
        return UEBooleanObject(self.val == other.val)
    
    def __init__(self, string: t.Any) -> None:
        self.val = float(string)

