from functools import wraps
from types import FunctionType, ModuleType
from typing import Any, Generic, TypeVar

from uel.object.object_parse import parse
from uel.object.uenumberobject import UENumberObject
from uel.tools.attr import AttributeOnly

from uel.modules import sequence

T = TypeVar("T")


class Wrap(Generic[T]):
    READ_ONLY = 0b01
    WRITE_ONLY = 0b10
    READ_AND_WRITE = 0b11

    def __init__(self) -> None:
        self.mode = self.READ_ONLY
        self._modules: dict[str, T] = {}

    def _add(self, name: str, module: T) -> None:
        self._modules[name] = module

    def get(self, name: str) -> T:
        assert self.mode & self.READ_ONLY
        return self._modules[name]

    def add(self, name: str, module: T) -> object:
        assert self.mode & self.WRITE_ONLY

        def decorator(func: FunctionType) -> FunctionType:
            self._add(name, func(name, module))
            return func

        return decorator

    def __call__(self, name: str) -> T:
        return self._modules[name]

    def __enter__(self) -> "Wrap":
        self.mode = self.WRITE_ONLY
        return AttributeOnly(self, ["add"])

    def __exit__(self, *args: Any) -> None:
        self.mode = self.READ_ONLY


wrap = Wrap[ModuleType]()
with wrap as modules:
   @modules.add("sequence", sequence)
   def _(name, mod): return mod
   
del modules
MAP: dict[str, ModuleType] = wrap._modules
