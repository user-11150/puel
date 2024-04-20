from uel.core.object.UEObject import UEObject

class UEStringObject(UEObject):
    def tp_bytecode(self):
        return ("string", self.val)
    def tp_str(self):
        return self.val
    def __init__(self, string):
        self.val = string
