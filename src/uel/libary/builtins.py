from uel.libary.pymodule import pymodule_get

BUILTIN_MODULES = {
    "time": (lambda: pymodule_get("_time", "libary")),
    "math": (lambda: pymodule_get("math", "libary"))
}
