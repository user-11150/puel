from uel.pyexceptions.Nerver import Nerver

# Impprt the classes
from uel.command.SystemArgument import SystemArgument
from uel.core.runner.ExecuteContext import ExecuteContext

# Import the types
from typing import List
from typing import Final

class Main:
    @staticmethod
    def main(argv: List[str]) -> None:
        # The function will execute build and execute
        
        sa: SystemArgument = SystemArgument(argv)
        sa.parserCommand()
        if sa.source_file is None:
            raise Nerver
        source_file: Final[str] = sa.source_file
        
        ectx: ExecuteContext = ExecuteContext()
        ectx.run_code_from_fd(open(source_file, "rt"), source_file)
