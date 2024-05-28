from typing import Callable

from uel.libary.pymodule import UEModuleNew, pymodule_get

BUILTIN_MODULES: dict[str, Callable[[], UEModuleNew]] = {
    "time": (lambda: pymodule_get("_time", "libary")),
    "math": (lambda: pymodule_get("math", "libary"))
}
