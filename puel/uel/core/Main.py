from uel.pyexceptions.Nerver import Nerver

# Impprt the classes
from uel.command.SystemArgument import SystemArgument
from uel.core.runner.ExecuteContext import ExecuteContext

# Import the types
from typing import List
from typing import Final
import os
import sys
from types import TracebackType, FrameType, CodeType

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
        try:
            ectx.run_code_from_fd(open(source_file, "rt"), source_file)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            os._exit(0)
        except Exception as e:
            print("UELRuntimeError(PythonError):", file=sys.stderr)
            def stack(stack_):
                def frame(f):
                    if f.f_back is None:
                        code = f.f_code
                        return f
                    return frame(f.f_back)
                f = frame(sys._getframe())
                typ = TracebackType(None, f, 1, 114514)
                return typ
                
            e.__traceback__ = stack(e.__traceback__)
            sys.excepthook(type(e), e, e.__traceback__)
