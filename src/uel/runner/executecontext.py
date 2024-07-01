from typing import IO, Any

from uel.constants import DEBUG
from uel.runner.task.buildcode import BuildCode
from uel.runner.task.runcode import RunCode

__all__ = ["ExecuteContext"]


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

    def run_code_from_fd(
        self, fd: IO[str], source: str, debug: bool = DEBUG
    ) -> Any:
        self.run_code_from_basic(source, fd.read(), debug=DEBUG)
