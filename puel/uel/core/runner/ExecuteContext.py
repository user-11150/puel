from uel.core.runner.task.BuildCode import BuildCode
from typing import IO

class ExecuteContext:
    def run_code_from_basic(self, fn: str, code: str) -> None:
        task: BuildCode = BuildCode(fn, code)
        task.run()

    def run_code_from_fd(self, fd: IO[str], source: str) -> None:
        self.run_code_from_basic(source, fd.read())