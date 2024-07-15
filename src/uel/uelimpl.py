from argparse import Namespace, ArgumentError
from abc import ABC,abstractmethod
from uel.compile import UELCode, uel_compile, UEL_SIMPLE_RUN_FLAGS

import typing as t

SOURCE_MODE = 1  # Run uel source codes
BINARY_MODE = 2  # A future feature

__all__ = ["SOURCE_MODE",
           "BINARY_MODE",
           "uel_run"]

class UELTask(ABC):
    @abstractmethod
    def run(self, *args: t.Any, **kwargs: t.Any) -> None:
        pass

class UELExecute(UELTask):
    UEL_EXEC_FILE = 1
    
    def __init__(self, args: list[t.Any], flag: int, mode: int) -> None:
        self.args = args
        self.flag = flag
        self.mode = mode
    
    def run(self, source = None) -> None:
        code = UELCode()
        if self.flag == UELExecute.UEL_EXEC_FILE:
            filename = self.args[0]
            code.co_filename = filename
            
            
            with open(filename, "rt", encoding=self.args[1]) as f:
                source = f.read()
        else:
            code.co_filename = "<string>"
        
        
        uel_compile(source, code, self.args[2], UEL_SIMPLE_RUN_FLAGS)
            

def uel_run(args: Namespace) -> None:
    execute = UELExecute([args.filename, args.encoding, args.verbose], flag=UELExecute.UEL_EXEC_FILE, mode=args.mode)
    
    execute.run()
