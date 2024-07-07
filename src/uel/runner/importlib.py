import builtins
import os
import re

import runpy

from uel.constants import ENCODING
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.libary.builtins import BUILTIN_MODULES
from importlib import import_module
from types import ModuleType
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.libary.default.patch import default_patch

__all__ = [
    "_read_string_from_file", "module_import", "path_abs", "UEModuleNew",
    "pymodule_get"
]


class UELModuleNewError(Exception):
    pass


class UELImportError(Exception):
    pass


class UEModuleNew:
    def __init__(self, pymodule: ModuleType) -> None:
        self.module = pymodule
        try:
            if not hasattr(pymodule, 'bytecodes'):
                raise UELImportError from \
                    AttributeError(
                        f"Object {pymodule} not have attribute 'bytecodes'")
        except Exception as e:
            raise UELModuleNewError("Module object of a non-composite UEModul"
                                    "e specification cannot be converted to a"
                                    " UELModule") \
                from e
        self.bytecodes: list[BytecodeInfo] = self.module.bytecodes


def pymodule_get(module_name: str) -> UEModuleNew:
    pymodule_name = f"uel.libary.{module_name}.module"
    patch_module_name = f"uel.libary.{module_name}.patch"
    module = import_module(pymodule_name)

    try:
        patch = import_module(patch_module_name).patch

    except ImportError:
        patch = default_patch

    patch(module)

    return UEModuleNew(module)


def _read_string_from_file(
    pathname: str, encoding: str | None = None
) -> str:
    emsgf = f"Cannot open file: {pathname}. %s"
    if not (os.path.exists(pathname) and os.path.isfile(pathname)):
        emsg = emsgf % "not exists or is directory"
        throw(UELRuntimeError(emsg))
        return ""
    try:
        with builtins.open(
            pathname, mode="rt", encoding=encoding or ENCODING
        ) as f:
            return f.read()
    except PermissionError as e:
        emsg = emsgf % e.__str__()
        throw(UELRuntimeError(emsg))
        return ""


def path_abs(relative_from: str, relative: str) -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(relative_from), relative)
    )


def module_import(name: str, from_there: str) -> list[BytecodeInfo]:
    from uel.runner.task.buildcode import BuildCode
    if name in BUILTIN_MODULES.keys():
        return BUILTIN_MODULES[name]().bytecodes
    if name.startswith("python::"):
        name = name[8:]
        path = path_abs(from_there, name)
        namespace = runpy.run_path(path)
        return namespace["bytecodes"]
    else:
        path = path_abs(from_there, name)
        source = _read_string_from_file(path)
        task = BuildCode(path, source)
        res = task.run(debug=False)[0]
        return res
