from uel.core.runner.task.BuildCode import BuildCode
from uel.core.runner.task.RunCode import RunCode

from typing import IO

class ExecuteContext:
    def run_code_from_basic(self, fn: str, code: str) -> None:
        bytecodeCompiler: BuildCode = BuildCode(fn, code)
        bytecodes = bytecodeCompiler.run()
        runner = RunCode()
        runner.run(bytecodes)

    def run_code_from_fd(self, fd: IO[str], source: str) -> None:
        self.run_code_from_basic(source, fd.read())