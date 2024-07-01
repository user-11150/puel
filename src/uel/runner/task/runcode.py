from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.runner.task.abstracttask import AbstractTask
from uel.runner.ueval import Ueval

__all__ = ["RunCode"]


class RunCode(AbstractTask):
    def run(self, tup: tuple[list[BytecodeInfo], str]) -> None:
        bytecodes, filename = tup
        execer = Ueval(bytecodes, filename=filename)
        execer.uelEval_EvalBytecodeDefault()
