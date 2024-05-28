from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.runner.task.AbstractTask import AbstractTask
from uel.core.runner.Ueval import Ueval


class RunCode(AbstractTask):

    def run(self, tup: tuple[list[BytecodeInfo], str]) -> None:
        bytecodes, filename = tup
        execer = Ueval(bytecodes, filename=filename)
        execer.uelEval_EvalBytecodeDefault()
