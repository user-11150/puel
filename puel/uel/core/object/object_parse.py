from uel.core.runner.Frame import Frame

from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.errors.runtime.throw import throw

from queue import Empty
from typing import Tuple

def parse(info: Tuple[str, str], frame: Frame):
    typ, val = info
    
    if typ == "stack_top":
        try:
            return parse(frame.gqueue.get_nowait(), frame)
        except Empty:
            throw(UELRuntimeError("[ValueError] At least one PUSH before TOP"))
    elif typ == "object":
        return val
    elif typ == "name":
        try:
            return frame.variables[val]
        except KeyError:
            throw(UELRuntimeError(f"[NameError] {val} is undefined"))
    else:
        raise ValueError
