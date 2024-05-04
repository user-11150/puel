from uel.core.runner.Frame import Frame
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.errors.runtime.throw import throw

from typing import *

def get_variable_from_frame(name, frame: Frame) -> Any:
    try:
        return frame.variables[name]
    except KeyError:
        if frame.prev_frame is None:
            throw(UELRuntimeError(f"NameError: {name} is not defined"))
        else:
            return get_variable_from_frame(name, frame.prev_frame)
