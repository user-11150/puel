import builtins
from typing import *

from uel.builder.ast.importnode import ImportNode
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.objects import UEObject
from uel.runner.frame import Frame

__all__ = ["get_variable_from_frame", "u_module_def"]


def get_variable_from_frame(name: object, frame: Frame) -> UEObject:
    current = frame
    while True:
        if current is None:
            throw(
                UELRuntimeError, f"Name {name} is not defined"
            )  # pragma: no cover
            raise SystemExit  # pragma: no cover
        try:
            return current.variables[name]  # type:ignore
        except KeyError:
            if current.prev_frame is None:
                throw(
                    UELRuntimeError, f"Name {name} is not defined"
                )  # pragma: no cover
                raise SystemExit  # pragma: no cover
            current = current.prev_frame
