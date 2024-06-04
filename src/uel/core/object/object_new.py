# pylint:disable=C0209

from typing import *

from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELMakeObjectError import UELMakeObjectError
from uel.core.object.UEBooleanObject import UEBooleanObject
from uel.core.object.UEFunctionObject import UEFunctionObject
from uel.core.object.UENumberObject import UENumberObject
from uel.core.object.UEObject import UEObject
from uel.core.object.UEStringObject import UEStringObject


def _CHECKOUT_TYP_TYPE(typ: str) -> None:
    assert IS_CAN_MAKE_OBJECT(typ), "Fuck you"
    if type(typ) is not str:
        raise TypeError("Arg 1 must be str")


def IS_CAN_MAKE_OBJECT(typ: str) -> bool:
    if (typ != "string" and typ != "number" and typ != "boolean" and
            typ != "function"):
        return False
    return True


def ueObjectGetConstructor(typ: str) -> Callable[..., UEObject]:
    if typ == "string":
        return UEStringObject
    elif typ == "number":
        return UENumberObject
    elif typ == "boolean":
        return UEBooleanObject
    elif typ == "function":
        return UEFunctionObject
    return UEObject  # Never


def __UEObjectNew(typ: str, val: Any) -> UEObject:
    constructor = ueObjectGetConstructor(typ)
    if constructor is UEFunctionObject:
        return constructor(*val)
    return constructor(val)


def uel_new_object(typ: str, val: Any) -> UEObject:
    _CHECKOUT_TYP_TYPE(typ)
    return __UEObjectNew(typ, val)
