from uel.core.errors.ThrowException import ThrowException

class RaiseError:
    def __init__(self,et,em,pos):
        ThrowException.throw(et(em,pos))