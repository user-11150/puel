import typing as t
from uel.core.object.UEObject import UEObject

class UENumberObject(UEObject):
    def tp_bytecode(self):
        return ("number", self.tp_str())

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
    
    def __init__(self, string: t.Any) -> None:
        self.val = float(string)

