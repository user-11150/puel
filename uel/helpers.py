from uel.core.runner.Frame import Frame
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.errors.runtime.throw import throw
from typing import *
from uel.core.builder.ast.ImportNode import ImportNode
from uel.core.runner.importlib import module_import

from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo

import builtins

def get_variable_from_frame(name, frame: Frame) -> Any:
    try:
        return frame.variables[name]
    except KeyError:
        if frame.prev_frame is None:
            throw(UELRuntimeError(f"NameError: {name} is not defined"))
        else:
            return get_variable_from_frame(name, frame.prev_frame)

def u_module_def(compiler: Any, node: ImportNode):
    for bytecode in module_import(node.libname, compiler.filename):
        bytecode: BytecodeInfo
        compiler.bytecode(bytecode.bytecode_type, bytecode.value)
