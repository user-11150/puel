import math

from uel.objects import parse
from uel.objects import UENumberObject
from uel.libary.helpers import make_exports

__all__ = ["PI", "sin", "bytecodes"]

PI = UENumberObject(math.pi)


def sin(f, n):
    i: UENumberObject = parse(n, f)
    i2 = i.val
    i3 = math.sin(i2)
    i4 = UENumberObject(i3)
    return i4


bytecodes = make_exports({"PI": PI, "sin": sin})
