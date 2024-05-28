import builtins
from typing import *

from uel.core.builder.ast.ImportNode import ImportNode
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.object.UEObject import UEObject
from uel.core.runner.Frame import Frame
from uel.core.runner.importlib import module_import


def get_variable_from_frame(name: object, frame: Frame) -> UEObject:
    try:
        return frame.variables[name]  # type: ignore
    except KeyError:
        if frame.prev_frame is None:
            throw(UELRuntimeError(f"NameError: {name} is not defined"))
            return UEObject()
        else:
            return get_variable_from_frame(name, frame.prev_frame)


def u_module_def(compiler: Any, node: ImportNode) -> None:
    for bytecode in module_import(node.libname, compiler.filename):
        compiler.bytecode(bytecode.bytecode_type, bytecode.value)
