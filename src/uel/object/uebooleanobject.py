# pylint:disable=C0415
from uel.object.ueobject import UEObject

TRUE = "true"
FALSE = "false"


class UEBooleanObject(UEObject):
    def tp_str(self):
        return str(self.val)

    def tp_add(self, other):
        # Avoid cyclic import
        from uel.object.uenumberobject import UENumberObject

        return UENumberObject(self.val + other.val)

    def __init__(self, val: str | bool):
        if type(val) is str:
            self.val = True if val == TRUE else False
        elif type(val) is bool:
            self.val = val
        else:
            raise TypeError(f"Unable to convert {type(val)} to Boolean")
