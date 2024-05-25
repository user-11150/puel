import os
import builtins
import re
import objprint

from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.errors.runtime.throw import throw
from uel.Constants import ENCODING

from uel.libary.pymodule import pymodule_get
from uel.libary.builtins import BUILTIN_MODULES

def _read_string_from_file(pathname: str, encoding=None) -> str:
    emsgf = f"Cannot open file: {pathname}. %s"
    if not (os.path.exists(pathname) and os.path.isfile(pathname)):
        emsg = emsgf % "not exists or is directory"
        throw(UELRuntimeError(emsg))
        return
    try:
        with builtins.open(pathname, mode="rt", encoding=encoding or ENCODING) as f:
            return f.read()
    except PermissionError as e:
        emsg = emsgf % e.__str__()
        throw(UELRuntimeError(emsg))
        return

def path_abs(relative_from, relative):
    return os.path.abspath(os.path.join(os.path.dirname(relative_from), relative))

def module_import(name, from_there):
    from uel.core.runner.task.BuildCode import BuildCode
    if name in BUILTIN_MODULES.keys():
        return BUILTIN_MODULES[name]().bytecodes
    path = path_abs(from_there, name)
    source = _read_string_from_file(path)
    task = BuildCode(path, source)
    res = task.run(debug=False)[0]
    return res
