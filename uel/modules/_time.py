from uel.modules.helpers import make_exports

import time

def uel_export_time(frame):
    raise
    from uel.core.object.object_new import uel_new_object
    return uel_new_object("number", time.time())

bytecodes = make_exports({
                "time": uel_export_time
            })
