from functools import wraps

from uel.tools.attr import AttributeOnly

from uel.core.object.object_parse import parse
from uel.core.object.UENumberObject import UENumberObject


class Wrap:
    READ_ONLY = 0b01
    WRITE_ONLY = 0b10
    READ_AND_WRITE = 0b11
    
    def __init__(self):
        self.mode = self.READ_ONLY
        self._modules = {}
    def _add(self,name, module):
        self._modules[name] = module

    def get(self, name):
        assert self.mode & self.READ_ONLY
        return self._modules[name]

    def add(self, name, module):
        assert self.mode & self.WRITE_ONLY
        
        def decorator(func):
            self._add(name, func(name, module))
            return func
        return decorator

    def __call__(self, name):
        return self._modules[name]

    def __enter__(self):
        self.mode = self.WRITE_ONLY
        return AttributeOnly(self, ["add"])

    def __exit__(self, *args):
        self.mode = self.READ_ONLY

wrap = Wrap()
with wrap as modules:
    pass # the uel modules with the c extensions
del modules
MAP = {
}

