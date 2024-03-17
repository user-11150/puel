from sys import stderr
from os import _exit

from uel.core.errors.UELBaseException import UELBaseException

STATUS = 1

class ThrowException:
    @staticmethod
    def throw(e: UELBaseException) -> None:
        stderr.write(str(e))
        stderr.write('\n')
        stderr.flush()
        
        exit()
