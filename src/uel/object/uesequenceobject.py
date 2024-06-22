from uel.object.ueobject import UEObject
from uel.impl.sequence import Sequence

class UESequenceObject(UEObject):
    def __init__(self):
        self.val = Sequence()

    def tp_str(self):
        string = ", ".join(map(lambda x: x.tp_str(), self.val.as_list()))
        return f"sequence({string})"
