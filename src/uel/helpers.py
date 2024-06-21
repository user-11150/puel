import builtins
from typing import *

from uel.builder.ast.importnode import ImportNode
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.object.ueobject import UEObject
from uel.runner.frame import Frame
from uel.runner.importlib import module_import


def get_variable_from_frame(name: object, frame: Frame) -> UEObject:
    current = frame
    while True:
        if current is None:
            throw(UELRuntimeError,
                  "Name {name} is not defined")  # pragma: no cover
            raise SystemExit  # pragma: no cover
        try:
            return current.variables[name]  # type:ignore
        except KeyError:
            if current.prev_frame is None:
                throw(UELRuntimeError,
                      "Name {name} is not defined")  # pragma: no cover
                raise SystemExit  # pragma: no cover
            current = current.prev_frame


def u_module_def(compiler: Any, node: ImportNode) -> None:
    for bytecode in module_import(node.libname, compiler.filename):
        compiler.bytecode(bytecode.bytecode_type, bytecode.value)
