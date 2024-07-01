from typing import Callable

from uel.libary.pymodule import UEModuleNew, pymodule_get

BUILTIN_MODULES: dict[str, Callable[[], UEModuleNew]] = {
    "time": lambda: pymodule_get("_time"),
    "math": lambda: pymodule_get("math"),
    "sequence": lambda: pymodule_get("sequence")
}
