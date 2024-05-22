from uel.core.runner.task.BuildCode import BuildCode
from uel.core.runner.task.RunCode import RunCode
from uel.Constants import DEBUG

from typing import IO, Any

class ExecuteContext:
    def run_code_from_basic(self, fn: str, code: str, debug) -> Any:
        bytecodeCompiler: BuildCode = BuildCode(fn, code)
        bytecodes = bytecodeCompiler.run(debug=debug)
        runner = RunCode()
        runner.run(bytecodes)

    def run_code_from_fd(self, fd: IO[str], source: str, debug=DEBUG) -> Any:
        self.run_code_from_basic(source, fd.read(), debug=DEBUG)