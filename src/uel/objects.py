# pylint:disable=C0209

from typing import *
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelmakeobjecterror import UELMakeObjectError
from queue import Empty
from typing import Tuple
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.runner.frame import Frame
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.runner.frame import Frame
from uel.runner.stack import Stack
from uel.impl.sequence import Sequence
from objprint import objstr

import typing as t

T = TypeVar("T")
__all__ = [
    "UEObject", "UEBooleanObject", "UECallableObject", "UEFunctionObject",
    "UENumberObject", "UESequenceObject", "UEStringObject",
    "IS_CAN_MAKE_OBJECT", "uel_new_object", "parse"
]

TRUE = "true"
FALSE = "false"


class UEObject:

    _create: Any

    def __new__(cls, *args) -> "UEObject":
        obj = object.__new__(cls)
        obj._create = args
        return obj

    def __reduce__(self) -> Tuple[type, Tuple[Any, ...]]:
        return self.__class__, self._create

    def __repr__(self):
        return self.tp_str()

    def __eq__(self, other):
        return self.tp_equal(other).val

    def tp_bytecode(self) -> Tuple[str, Any]:
        return "object", self

    def tp_str(self) -> Any:
        return_string = hex(id(self))
        classname = self.__class__.__name__[2:-6]
        return f"[{classname.lower()} {classname.title()}]"

    def tp(self, typ: type[T]) -> T:
        return self  # type: ignore


class UEBooleanObject(UEObject):
    def tp_str(self):
        return str(self.val)

    def tp_add(self, other):
        # Avoid cyclic import
        from uel.objects import UENumberObject

        return UENumberObject(self.val + other.val)

    def __init__(self, val: str | bool):
        if type(val) is str:
            self.val = True if val == TRUE else False
        elif type(val) is bool:
            self.val = val
        else:
            raise TypeError(f"Unable to convert {type(val)} to Boolean")


class UECallableObject(UEObject):
    def __init__(self) -> None:
        pass

    def tp_call(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class UEFunctionObject(UECallableObject):
    def __init__(
        self, args: List[str], bytecodes: List[BytecodeInfo]
    ) -> None:
        self.args = args
        self.bytecodes = bytecodes

    def tp_call(self, ueval, frame: Frame, args: list[UEObject]) -> None:
        from uel.runner.ueval import Ueval

        if len(args) != len(self.args):
            throw(
                UELRuntimeError(
                    f"Only {len(self.args)} parameters are accepted,"
                    f"but there are {args} arguments."
                )
            )
        frame = Frame(
            stack=Stack(),
            idx=0,
            bytecodes=self.bytecodes,
            prev_frame=frame,
            filename=frame.filename,
            variables=dict(
                zip(self.args, (parse(x, frame) for x in args))
            )
        )
        ueval.frame = frame


class UENumberObject(UEObject):
    def tp_str(self):
        return str(self.val)

    def tp_add(self, other):
        return UENumberObject(
            self.val +
            (other.val if isinstance(other, UENumberObject) else other)
        )

    def tp_minus(self, other):
        return UENumberObject(
            self.val -
            (other.val if isinstance(other, UENumberObject) else other)
        )

    def tp_mult(self, other):
        return UENumberObject(
            self.val *
            (other.val if isinstance(other, UENumberObject) else other)
        )

    def tp_div(self, other):
        return UENumberObject(
            self.val /
            (other.val if isinstance(other, UENumberObject) else other)
        )

    def tp_equal(self, other):
        if not runtime_type_check(other, type(self)):
            return UEBooleanObject(False)
        return UEBooleanObject(self.val == other.val)

    def __init__(self, string: t.Any) -> None:
        if type(string) in (int, float):
            self.val = string
        else:
            if "." not in string:
                self.val = int(string)
            else:
                self.val = float(string)


class UESequenceObject(UEObject):
    def __init__(self):
        self.val = Sequence()

    def tp_str(self):
        string = ", ".join(map(lambda x: x.tp_str(), self.val.as_list()))
        return f"sequence({string})"


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
        if (
            runtime_type_check(other, UEStringObject) and
            other.val == self.val
        ):
            return UEBooleanObject(True)
        return UEBooleanObject(False)


def _CHECKOUT_TYP_TYPE(typ: str) -> None:
    assert IS_CAN_MAKE_OBJECT(typ), "Fuck you"
    if type(typ) is not str:
        raise TypeError("Arg 1 must be str")


def IS_CAN_MAKE_OBJECT(typ: str) -> bool:
    if (
        typ != "string" and typ != "number" and typ != "boolean" and
        typ != "function"
    ):
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


def parse(info: tuple[str, UEObject] | UEObject, frame: Frame) -> UEObject:
    from uel.helpers import get_variable_from_frame
    if not (isinstance(info, tuple)):
        return info
    typ, val = info

    if typ == "stack_top":
        try:
            return parse(frame.gqueue.get_nowait(), frame)
        except Empty:
            throw(
                UELRuntimeError(
                    "[ValueError] At least one PUSH before TOP"
                )
            )
    elif typ == "object":
        return val
    elif typ == "name":
        return get_variable_from_frame(val, frame)
    raise ValueError
