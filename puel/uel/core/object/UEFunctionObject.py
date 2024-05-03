from uel.core.object.UECallableObject import UECallableObject
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError
from uel.core.runner.Frame import Frame
from uel.core.runner.Stack import Stack
from uel.core.object.object_parse import parse
from typing import List

class UEFunctionObject(UECallableObject):
    def __init__(self, args: List[str], bytecodes: List[BytecodeInfo]) -> None:
        self.args = args
        self.bytecodes = bytecodes

    def tp_str(self):
        return f"<function: disassembly of {self.bytecodes}>"

    def tp_call(self, frame, args):
        from uel.core.runner.Ueval import Ueval

        if len(args) != len(self.args):
            throw(UELRuntimeError(f"Only {len(self.args)} parameters are accepted,"
                                  f"but there are {args} arguments."))
        frame = Frame(
            Stack(),
            0,
            self.bytecodes,
            frame, 
            dict(
                zip(
                    self.args,
                    (parse(x, frame) for x in args)
                )
            )
        )
        u_eval = Ueval(self.bytecodes, frame)
        u_eval.uelEval_EvalBytecodeDefault()
