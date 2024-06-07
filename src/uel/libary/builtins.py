from typing import Callable

from uel.libary.pymodule import UEModuleNew, pymodule_get
from uel._builtins.libary_and_modules import Builtins

BUILTIN_MODULES: dict[str, Callable[[], UEModuleNew]] = Builtins.all()
