import time

from uel.libary.helpers import make_exports

__all__ = ["uel_export_time", "bytecodes"]


def uel_export_time(frame):
    from uel.objects import uel_new_object
    return uel_new_object("number", time.time())


bytecodes = make_exports({"time": uel_export_time})
