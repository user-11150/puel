from queue import Empty
from typing import Tuple

from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.object.ueobject import UEObject
from uel.runner.frame import Frame
from uel.helpers import get_variable_from_frame


def parse(info: tuple[str, UEObject] | UEObject, frame: Frame) -> UEObject:
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
