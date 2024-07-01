from importlib import import_module
from types import ModuleType

from uel.builder.bytecode.bytecodeinfo import BytecodeInfo

from uel.libary.default.patch import default_patch

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
