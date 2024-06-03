from typing import List

from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.object.object_parse import parse
from uel.core.object.UECallableObject import UECallableObject
from uel.core.object.UEObject import UEObject
from uel.core.runner.Frame import Frame
from uel.core.runner.Stack import Stack

from objprint import objstr


class UEFunctionObject(UECallableObject):

    def __init__(self, args: List[str], bytecodes: List[BytecodeInfo]) -> None:
        self.args = args
        self.bytecodes = bytecodes

    def tp_call(self, ueval, frame: Frame, args: list[UEObject]) -> None:
        from uel.core.runner.Ueval import Ueval

        if len(args) != len(self.args):
            throw(
                UELRuntimeError(
                    f"Only {len(self.args)} parameters are accepted,"
                    f"but there are {args} arguments."))
        frame = Frame(stack=Stack(),
                      idx=0,
                      bytecodes=self.bytecodes,
                      prev_frame=frame,
                      filename=frame.filename,
                      variables=dict(
                          zip(self.args, (parse(x, frame) for x in args))))
        ueval.frame = frame
