from uel.core.runner.task.BuildCode import BuildCode
from _io import TextIOWrapper

class ExecuteContext:
    def run_code_from_basic(self, fn: str, code: str) -> None:
        task: BuildCode = BuildCode(fn, code)
        task.run()

    def run_code_from_fd(self, fd: TextIOWrapper, source: str) -> None:
        self.run_code_from_basic(source, fd.read())