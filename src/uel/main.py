import os
import sys
# Import the types
from typing import List

from uel.ueargparse import UEArgParser, UETask
from uel.hook.initiation import initialization

__all__ = ["Main"]


class Main:
    @staticmethod
    def main(argv: List[str]) -> None:
        initialization()

        parser = UEArgParser(argv[1:])
        try:
            task = UETask(parser)
            task.run()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            os._exit(0)
