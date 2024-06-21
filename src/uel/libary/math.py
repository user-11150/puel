import math

from uel.object.object_parse import parse
from uel.object.uenumberobject import UENumberObject
from uel.libary.helpers import make_exports

PI = UENumberObject(math.pi)


def sin(f, n):
    i: UENumberObject = parse(n, f)
    i2 = i.val
    i3 = math.sin(i2)
    i4 = UENumberObject(i3)
    return i4


bytecodes = make_exports({"PI": PI, "sin": sin})
