#pylint:disable=C0209

from uel.core.object.UENumberObject import UENumberObject
from uel.core.object.UEStringObject import UEStringObject
from uel.core.object.UEBooleanObject import UEBooleanObject

from uel.core.errors.runtime.UELMakeObjectError import UELMakeObjectError
from uel.core.errors.runtime.throw import throw

def _CHECKOUT_TYP_TYPE(typ):
    assert IS_CAN_MAKE_OBJECT(typ), "Fuck you"
    if type(typ) is not str:
        raise TypeError("Arg 1 must be str")

def IS_CAN_MAKE_OBJECT(typ: str):
    if (typ != "string"
      and typ != "number"
      and typ != "boolean"):
        return False
    return True

def ueObjectGetConstructor(typ):
    if typ == "string":
        return UEStringObject
    elif typ == "number":
        return UENumberObject
    elif typ == "boolean":
        return UEBooleanObject

def __UEObjectNew(typ, val):
    constructor = ueObjectGetConstructor(typ)
    return constructor(val)

def uel_new_object(typ, val):
    _CHECKOUT_TYP_TYPE(typ)
    return __UEObjectNew(typ, val)
