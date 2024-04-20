from uel.core.object.UENumberObject import UENumberObject
from uel.core.object.UEStringObject import UEStringObject

from typing import Tuple

def parse(info: Tuple[str, str]):
    typ, val = info
    if typ == "number":
        constructor = UENumberObject
    elif typ == "string":
        constructor = UEStringObject
    else:
        raise ValueError
    return constructor(val)
