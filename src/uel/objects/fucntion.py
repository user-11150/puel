from __future__ import annotations

from uel.objects.object import UELObject
from uel.virtual_machine.frames import Frame
from typing import TYPE_CHECKING
from uel.objects.none import uel_none

if TYPE_CHECKING:
    from uel.virtual_machine.uel_eval import UELEval


class UELFunction(UELObject):
    tp_name = "function"

    def __init__(self, args, code):
        self._args = args
        self._code = code

    def tp_call(self, executor: UELEval, args: list[UELObject]):
        v = {}
        i = -1
        for a in self._args:
            v[a] = args[i := i + 1]
        frame = Frame(
            f_back=executor.frame,
            f_code=self._code,
            f_lasti=0,
            f_vars=v
        )
        executor.frame = frame


class UELPyFunction(UELObject):
    tp_name = 'built-in function'

    def __init__(self, f):
        self.f = f

    def tp_call(self, executor: UELEval, args):
        retval = self.f(executor, *args)
        if retval is None:
            retval = uel_none
        executor.push_stack(retval)


uel_func_from_pyfunc = UELPyFunction
