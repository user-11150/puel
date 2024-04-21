from uel.core.object.UEObject import UEObject

TRUE = "true"
FALSE = "false"

class UEBooleanObject(UEObject):
    def tp_bytecode(self):
        return ("boolean", self.val)

    def tp_str(self):
        return str(self.val)

    def __init__(self, val: str):
        self.val = True if val == TRUE else FALSE
