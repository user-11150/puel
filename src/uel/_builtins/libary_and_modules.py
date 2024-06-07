import os
from uel.Constants import DIRNAME

class Builtins:
    @staticmethod
    def all():
        return _get_all_modules()

def _get_all_modules():
    from uel.libary.pymodule import pymodule_get
    return {
             "time": (lambda: pymodule_get("_time", "libary")),
             "math": (lambda: pymodule_get("math", "libary"))
           }
