from uel.objects import parse
from uel.objects import UESequenceObject
from uel.objects import UEBooleanObject
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.libary.helpers import make_exports

def contains(frame, x, y):
    left = parse(x, frame)
    right = parse(y, frame)
    
    if type(right) is UESequenceObject:
        if type(left) is UESequenceObject:
            rightl = right.val.as_list()
            leftl = left.val.as_list()
            return UEBooleanObject(leftl in rightl)
    throw(UELRuntimeError, "x and y must be sequence")

bytecodes = make_exports({
    "contains": contains
})
