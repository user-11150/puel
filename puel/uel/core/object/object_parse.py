from uel.core.object.UENumberObject import UENumberObject
from uel.core.object.UEStringObject import UEStringObject

from uel.core.runner.Frame import Frame

from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.errors.runtime.throw import throw

from queue import Empty
from typing import Tuple

def parse(info: Tuple[str, str], frame: Frame):
    typ, val = info
    if typ == "number":
        constructor = UENumberObject
    elif typ == "string":
        constructor = UEStringObject
    elif typ == "stack_top":
        try:
            return parse(frame.gqueue.get_nowait(), frame)
        except Empty:
            throw(UELRuntimeError("[ValueError] At least one PUSH before TOP"))
    elif typ == "name":
        try:
            return frame.variables[val]
        except KeyError:
            throw(UELRuntimeError(f"[NameError] {val} is undefined"))
    else:
        raise ValueError
    return constructor(val)
