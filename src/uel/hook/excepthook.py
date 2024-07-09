import sys
from uel.errors.uelbaseexception import UELBaseException
from uel.errors.ueerror_setstring import UEErr_SetString

default_excepthook = sys.excepthook


def excepthook(exctype, value, traceback):
    if issubclass(exctype, UELBaseException):
        # traceback.walk_stack(traceback)
        UEErr_SetString(value)
        return

    default_excepthook(exctype, value, traceback)
