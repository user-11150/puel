from uel.core.runner.task.AbstractTask import AbstractTask

from uel.core.runner.Ueval import Ueval

class RunCode(AbstractTask):
    def run(self, tup):
        bytecodes, filename = tup
        execer = Ueval(bytecodes, filename=filename)
        execer.uelEval_EvalBytecodeDefault()
