from typing import List

from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.errors.runtime.throw import throw
from uel.errors.runtime.uelruntimeerror import UELRuntimeError
from uel.object.object_parse import parse
from uel.object.uecallableobject import UECallableObject
from uel.object.ueobject import UEObject
from uel.runner.frame import Frame
from uel.runner.stack import Stack

from objprint import objstr


class UEFunctionObject(UECallableObject):

    def __init__(self, args: List[str], bytecodes: List[BytecodeInfo]) -> None:
        self.args = args
        self.bytecodes = bytecodes

    def tp_call(self, ueval, frame: Frame, args: list[UEObject]) -> None:
        from uel.runner.ueval import Ueval

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
