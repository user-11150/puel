from typing import IO, Any

from uel.Constants import DEBUG
from uel.core.runner.task.BuildCode import BuildCode
from uel.core.runner.task.RunCode import RunCode


class ExecuteContext:

    def run_code_from_basic(self, fn: str, code: str, debug: bool) -> Any:
        bytecodeCompiler: BuildCode = BuildCode(fn, code)
        bytecodes = bytecodeCompiler.run(debug=debug)
        runner = RunCode()
        runner.run(bytecodes)

    def build_bytecodes(self, fn, code, debug):
        bytecodeCompiler: BuildCode = BuildCode(fn, code)
        bytecodes = bytecodeCompiler.run(debug=debug)
        return bytecodes

    def run_bytecodes(self, bytecodes):
        RunCode().run(bytecodes)

    def run_code_from_fd(self,
                         fd: IO[str],
                         source: str,
                         debug: bool = DEBUG) -> Any:
        self.run_code_from_basic(source, fd.read(), debug=DEBUG)
