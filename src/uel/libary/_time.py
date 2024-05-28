import time

from uel.libary.helpers import make_exports


def uel_export_time(frame):
    from uel.core.object.object_new import uel_new_object
    return uel_new_object("number", time.time())


bytecodes = make_exports({"time": uel_export_time})
