from os import _exit
from sys import stderr

from uel.errors.uelbaseexception import UELBaseException
from uel.errors.uelbuildtimeexception import UELBuildtimeException
import objprint

STATUS = 1

__all__ = ["ThrowException"]


class ThrowException:
    @staticmethod
    def throw(e: UELBaseException) -> None:
        raise e
