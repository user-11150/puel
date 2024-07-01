from os import _exit
from sys import stderr

from uel.errors.uelbaseexception import UELBaseException

STATUS = 1

__all__ = ["ThrowException"]


class ThrowException:
    @staticmethod
    def throw(e: UELBaseException) -> None:
        stderr.write(str(e))
        stderr.write('\n')
        stderr.flush()

        _exit(1)
