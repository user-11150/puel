from importlib import import_module

class UELModuleNewError(Exception):
    pass

class UELImportError(Exception):
    pass

class UEModuleNew:
    def __init__(self, pymodule):
        self.module = pymodule
        try:
            if not hasattr(pymodule, 'bytecodes'):
                raise UELImportError from \
                    AttributeError(f"Object {pymodule} not have attribute 'bytecodes'")
        except Exception as e:
            raise UELModuleNewError("Module object of a non-composite UEModul"
                                    "e specification cannot be converted to a"
                                    " UELModule") \
                  from e
            

    @property
    def bytecodes(self):
        return self.module.bytecodes

def pymodule_get(module_name, prefix):
    if prefix == "libary":
        
        pymodule_name = f"uel.{prefix}.{module_name}"
        module = import_module(pymodule_name)
    else:
        from uel.modules.map import MAP
        module = MAP[module_name]
    return UEModuleNew(module)
