from uel.core.object.UEObject import UEObject

class UEStringObject(UEObject):
    def tp_str(self):
        return self.val
    def __init__(self, string):
        self.val = string
