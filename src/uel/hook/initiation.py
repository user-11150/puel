import sys

from uel.hook.excepthook import excepthook


def initialization():
    sys.excepthook = excepthook
