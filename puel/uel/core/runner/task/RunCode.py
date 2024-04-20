from uel.core.runner.task.AbstractTask import AbstractTask

from uel.core.runner.Ueval import Ueval

class RunCode(AbstractTask):
    def run(self, bytecodes):
        execer = Ueval(bytecodes)
        execer.uelEval_EvalBytecodeDefault()
