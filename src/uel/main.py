import os
import sys
# Import the types
from typing import List

from uel.ueargparse import UEArgParser, UETask

__all__ = ["Main"]


class Main:
    @staticmethod
    def main(argv: List[str]) -> None:
        parser = UEArgParser(argv[1:])
        try:
            task = UETask(parser)
            task.run()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            os._exit(0)
        except Exception as e:
            print("UELRuntimeError(PythonError):", file=sys.stderr)
            sys.excepthook(type(e), e, e.__traceback__)
